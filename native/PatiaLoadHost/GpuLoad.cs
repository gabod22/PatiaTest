using System.Diagnostics;
using System.Runtime.InteropServices;
using Vortice.Direct3D;
using Vortice.Direct3D11;
using Vortice.D3DCompiler;
using Vortice.DXGI;
using static Vortice.DXGI.DXGI;
using static Vortice.Direct3D11.D3D11;

namespace PatiaLoadHost;

public record GpuInfo(string Id, string Name, ulong DedicatedMemory);

internal sealed class GpuLoad : IDisposable
{
    [DllImport("winmm.dll")] private static extern uint timeBeginPeriod(uint period);
    [DllImport("winmm.dll")] private static extern uint timeEndPeriod(uint period);
    private static string Identity(Vortice.Luid luid) => (((ulong)(uint)luid.HighPart << 32) | luid.LowPart).ToString("X");
    private readonly CancellationTokenSource cancellation = new();
    private readonly Thread worker;
    private readonly TaskCompletionSource ready = new(TaskCreationOptions.RunContinuationsAsynchronously);
    private double duty;
    private Exception? failure;
    public double Duty { get => Volatile.Read(ref duty); set => Volatile.Write(ref duty, Math.Clamp(value, 0, 1)); }
    public void Check() { if (failure is not null) throw new InvalidOperationException("Falló la carga gráfica: " + failure.Message, failure); }
    public static GpuInfo[] Enumerate()
    {
        using var factory = CreateDXGIFactory1<IDXGIFactory1>();
        var result = new List<GpuInfo>();
        for (uint i = 0; factory.EnumAdapters1(i, out var adapter).Success; i++)
        {
            using (adapter)
            {
                var desc = adapter.Description1;
                if ((desc.Flags & AdapterFlags.Software) != 0) continue;
                result.Add(new(Identity(desc.Luid), desc.Description, desc.DedicatedVideoMemory));
            }
        }
        return result.ToArray();
    }
    public GpuLoad(string id)
    {
        worker = new Thread(() => Run(id)) { IsBackground = true, Priority = ThreadPriority.BelowNormal, Name = "Carga GPU" };
        worker.Start();
        try { ready.Task.WaitAsync(TimeSpan.FromSeconds(8)).GetAwaiter().GetResult(); }
        catch { cancellation.Cancel(); worker.Join(1000); throw; }
    }
    private void Run(string id)
    {
        bool timerResolution = timeBeginPeriod(1) == 0;
        try
        {
            using var factory = CreateDXGIFactory1<IDXGIFactory1>();
            IDXGIAdapter1? selected = null;
            for (uint i = 0; factory.EnumAdapters1(i, out var adapter).Success; i++)
            {
                if (Identity(adapter.Description1.Luid) == id) { selected = adapter; break; }
                adapter.Dispose();
            }
            using var physical = selected ?? throw new InvalidOperationException("GPU no disponible.");
            D3D11CreateDevice(physical, DriverType.Unknown, DeviceCreationFlags.None, [FeatureLevel.Level_11_0], out ID3D11Device device, out ID3D11DeviceContext context).CheckError();
            using (device)
            using (context)
            {
                const string source = "RWStructuredBuffer<float> data : register(u0); [numthreads(64,1,1)] void main(uint3 id : SV_DispatchThreadID) { float x = float(id.x)*0.001+0.123; [loop] for(uint i=0;i<256;i++) x=frac(x*1.00013+0.1234); data[id.x]=x; }";
                string adaptiveSource = source.Replace("[numthreads", "cbuffer Settings : register(b0) { uint iterations; uint3 padding; }; [numthreads").Replace("i<256", "i<iterations");
                var bytecode = Compiler.Compile(adaptiveSource, "main", "PatiaLoad", "cs_5_0");
                using var shader = device.CreateComputeShader(bytecode.Span);
                using var buffer = device.CreateBuffer(65536 * 4, BindFlags.UnorderedAccess, ResourceUsage.Default, CpuAccessFlags.None, ResourceOptionFlags.BufferStructured, 4);
                using var uav = device.CreateUnorderedAccessView(buffer);
                using var query = device.CreateQuery(QueryType.Event);
                using var beginTime = device.CreateQuery(QueryType.Timestamp);
                using var endTime = device.CreateQuery(QueryType.Timestamp);
                using var disjoint = device.CreateQuery(QueryType.TimestampDisjoint);
                using var settings = device.CreateBuffer(16, BindFlags.ConstantBuffer);
                context.CSSetShader(shader);
                context.CSSetUnorderedAccessView(0, uav);
                context.CSSetConstantBuffer(0, settings);
                int groups = 64;
                uint iterations = 256;
                bool probe = true;
                while (!cancellation.IsCancellationRequested)
                {
                    double fraction = probe ? .05 : Duty;
                    if (fraction == 0) { cancellation.Token.WaitHandle.WaitOne(20); continue; }
                    var timer = Stopwatch.StartNew();
                    context.UpdateSubresource(new Settings { Iterations = iterations, Pad1 = 0, Pad2 = 0, Pad3 = 0 }, settings);
                    context.Begin(disjoint); context.End(beginTime);
                    context.Dispatch((uint)groups, 1, 1);
                    context.End(endTime); context.End(disjoint);
                    context.End(query); context.Flush();
                    while (!context.GetData(query, out int completed) || completed == 0)
                    {
                        if (cancellation.IsCancellationRequested) return;
                        if (timer.ElapsedMilliseconds > 1000) throw new TimeoutException("La GPU no respondió a un paquete breve.");
                        Thread.Yield();
                    }
                    double ms = timer.Elapsed.TotalMilliseconds;
                    if (context.GetData(disjoint, out QueryDataTimestampDisjoint clock) && !clock.Disjoint && clock.Frequency > 0 &&
                        context.GetData(beginTime, out ulong begin) && context.GetData(endTime, out ulong end))
                        ms = (end - begin) * 1000.0 / clock.Frequency;
                    ms = Math.Max(.01, ms);
                    if (ms > 10) { if (iterations > 256) iterations /= 2; else groups = Math.Max(1, groups / 2); }
                    else if (ms < 3) { if (groups < 1024) groups *= 2; else iterations = Math.Min(65536u, iterations * 2); }
                    if (probe) { probe = false; ready.TrySetResult(); }
                    double rest = ms / fraction - timer.Elapsed.TotalMilliseconds;
                    if (rest > 0)
                    {
                        double until = timer.Elapsed.TotalMilliseconds + Math.Min(100, rest);
                        while (!cancellation.IsCancellationRequested && timer.Elapsed.TotalMilliseconds < until)
                            if (until - timer.Elapsed.TotalMilliseconds > 2) Thread.Sleep(1); else Thread.Yield();
                    }
                }
            }
        }
        catch (Exception ex) { failure = ex; ready.TrySetException(ex); }
        finally { ready.TrySetCanceled(); if (timerResolution) timeEndPeriod(1); }
    }
    public void Dispose()
    {
        Duty = 0; cancellation.Cancel();
        if (!worker.Join(2000)) throw new TimeoutException("La GPU no terminó; se debe cerrar el auxiliar.");
        cancellation.Dispose();
    }
    private struct Settings { public uint Iterations, Pad1, Pad2, Pad3; }
}
