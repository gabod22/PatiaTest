using System.Diagnostics;
using System.Text;
using System.Text.Json;
using PatiaLoadHost;

Console.InputEncoding = Encoding.UTF8;
Console.OutputEncoding = new UTF8Encoding(false);
var json = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower, PropertyNameCaseInsensitive = true };
if (args.Contains("--self-test"))
{
    SelfTests.Run();
    return;
}
using var engine = new Engine();
while (Console.ReadLine() is { } line)
{
    string id = "", operation = "";
    try
    {
        using var doc = JsonDocument.Parse(line);
        var request = doc.RootElement;
        id = request.GetProperty("id").GetString() ?? "";
        operation = request.GetProperty("operation").GetString() ?? "";
        if (request.GetProperty("version").GetInt32() != 1) throw new InvalidOperationException("Versión incompatible.");
        engine.Ping();
        object result = operation switch
        {
            "capabilities" => engine.Capabilities(),
            "start" or "update" => engine.Start(JsonSerializer.Deserialize<LoadConfig>(request.GetProperty("config"), json)!),
            "status" => engine.Status(),
            "stop" or "shutdown" => engine.Stop(),
            _ => throw new InvalidOperationException("Operación desconocida.")
        };
        Console.WriteLine(JsonSerializer.Serialize(new { version = 1, id, operation, ok = true, data = result }, json));
        if (operation == "shutdown") break;
    }
    catch (Exception ex)
    {
        try { engine.Stop(); } catch { }
        Console.WriteLine(JsonSerializer.Serialize(new { version = 1, id, operation, ok = false, error = ex.Message }, json));
    }
}

namespace PatiaLoadHost
{
    public record LoadConfig(double CpuTarget = 0, double GpuTarget = 0, int InitialCores = 0, string? GpuId = null);
    internal sealed class Engine : IDisposable
    {
        private readonly PhysicalCore[] cores = Topology.Read();
        private readonly Counters counters = new();
        private CpuLoad? cpu;
        private GpuLoad? gpu;
        private LoadConfig config = new();
        private readonly Queue<double> cpuAverage = new(), gpuAverage = new();
        private long ping = Stopwatch.GetTimestamp();
        private readonly Timer watchdog;
        private bool active;
        private string? error;
        private TimeSpan previousCpuTime;
        private long previousCpuTick;
        private readonly Process ownProcess = Process.GetCurrentProcess();
        public Engine() => watchdog = new Timer(_ =>
        {
            // Exit also covers blocked native calls; Windows reclaims every worker/context.
            if (Volatile.Read(ref active) && Stopwatch.GetElapsedTime(Interlocked.Read(ref ping)).TotalSeconds > 5) Environment.Exit(3);
        }, null, 1000, 500);
        public void Ping() => Interlocked.Exchange(ref ping, Stopwatch.GetTimestamp());
        public object Capabilities()
        {
            GpuInfo[] adapters = []; string? gpuError = null;
            try { adapters = GpuLoad.Enumerate(); } catch (Exception ex) { gpuError = ex.Message; }
            return new { physical_cores = cores.Length, logical_cpus = cores.Sum(c => c.Threads.Length), topology = cores,
                gpus = adapters, gpu_error = gpuError, cpu_counter = counters.CpuAvailable, gpu_counter = counters.GpuAvailable };
        }
        public object Start(LoadConfig value)
        {
            Stop();
            if (!double.IsFinite(value.CpuTarget) || !double.IsFinite(value.GpuTarget) || value.CpuTarget is < 0 or > 100 || value.GpuTarget is < 0 or > 100 || value.InitialCores < 0 || value.InitialCores > cores.Length)
                throw new ArgumentException("Objetivos o núcleos no válidos.");
            config = value; error = null;
            if (config.CpuTarget > 0 && !counters.CpuAvailable) throw new InvalidOperationException("No se puede medir el uso global de CPU.");
            if (config.GpuTarget > 0)
            {
                if (!counters.GpuAvailable || config.GpuId is null) throw new InvalidOperationException("No se puede medir la GPU seleccionada.");
                gpu = new GpuLoad(config.GpuId);
            }
            Thread.Sleep(1000);
            var sample = counters.Sample(config.GpuId);
            if (config.CpuTarget > 0 && sample.Cpu is null) throw new InvalidOperationException("No hay una medición válida de CPU.");
            if (config.GpuTarget > 0 && sample.Gpu is null)
            {
                Thread.Sleep(1000); sample = counters.Sample(config.GpuId);
                if (sample.Gpu is null) throw new InvalidOperationException("La GPU no expone contadores válidos; no se generará carga sin medición.");
            }
            cpu = new CpuLoad(cores);
            cpu.Configure(config.InitialCores, config.CpuTarget, sample.Cpu ?? 0);
            if (gpu is not null) gpu.Duty = Math.Clamp((config.GpuTarget - (sample.Gpu ?? 0)) / 100, 0, 1);
            cpuAverage.Clear(); gpuAverage.Clear(); Ping(); Volatile.Write(ref active, true);
            previousCpuTime = ownProcess.TotalProcessorTime; previousCpuTick = Stopwatch.GetTimestamp();
            return new { state = "running" };
        }
        public object Status()
        {
            var sample = counters.Sample(config.GpuId);
            static double? Smooth(Queue<double> queue, double? value)
            {
                if (value is null) { queue.Clear(); return null; }
                queue.Enqueue(value.Value); while (queue.Count > 3) queue.Dequeue(); return queue.Average();
            }
            double? actualCpu = Smooth(cpuAverage, sample.Cpu), actualGpu = Smooth(gpuAverage, sample.Gpu);
            var processTime = ownProcess.TotalProcessorTime;
            double? generated = active && previousCpuTick != 0 ? Math.Clamp((processTime - previousCpuTime).TotalSeconds /
                Math.Max(.001, Stopwatch.GetElapsedTime(previousCpuTick).TotalSeconds) / cores.Sum(c => c.Threads.Length) * 100, 0, 100) : null;
            previousCpuTime = processTime; previousCpuTick = Stopwatch.GetTimestamp();
            double? externalCpu = Feedback.ExternalCpu(sample.Cpu, generated);
            if (active)
            {
                gpu?.Check();
                if (config.CpuTarget > 0 && externalCpu > config.CpuTarget) cpu?.Pause();
                else if (config.CpuTarget > 0 && actualCpu is not null) cpu?.Adjust(config.CpuTarget, actualCpu.Value, sample.Cpu);
                if (config.GpuTarget > 0 && actualGpu is not null && gpu is not null) gpu.Duty = Feedback.Next(gpu.Duty, config.GpuTarget, actualGpu.Value);
            }
            return new { state = active ? "running" : "stopped", cpu_actual = actualCpu, gpu_actual = actualGpu,
                cpu_raw = sample.Cpu, gpu_raw = sample.Gpu, cpu_target = config.CpuTarget, gpu_target = config.GpuTarget,
                active_cores = config.CpuTarget > 0 && active && cpu?.Duty > 0 ? cpu.ActiveCores : 0,
                cpu_duty = cpu?.Duty ?? 0, gpu_duty = gpu?.Duty ?? 0, error,
                cpu_generated = generated,
                cpu_external_estimate = externalCpu,
                limitation = active && ((externalCpu > config.CpuTarget && config.CpuTarget > 0) ||
                                       (actualGpu > config.GpuTarget + 10 && gpu?.Duty == 0 && config.GpuTarget > 0)) ? "Actividad externa superior al objetivo" :
                             active && ((actualCpu > config.CpuTarget + 5 && config.CpuTarget > 0) ||
                                       (actualGpu > config.GpuTarget + 10 && config.GpuTarget > 0)) ? "Objetivo excedido; reduciendo carga" : null };
        }
        public object Stop()
        {
            Volatile.Write(ref active, false);
            try { cpu?.Dispose(); } finally { cpu = null; try { gpu?.Dispose(); } finally { gpu = null; } }
            return new { state = "stopped" };
        }
        public void Dispose() { try { Stop(); } finally { watchdog.Dispose(); counters.Dispose(); ownProcess.Dispose(); } }
    }
}
