using System.Diagnostics;

namespace PatiaLoadHost;

internal sealed class CpuLoad(PhysicalCore[] cores) : IDisposable
{
    private readonly CancellationTokenSource cancellation = new();
    private readonly List<Thread> workers = [];
    private int active;
    private double duty;
    private Exception? failure;
    public int ActiveCores => active;
    public int LogicalCount => cores.Sum(c => c.Threads.Length);
    public double Capacity => cores.Take(active).Sum(c => c.Threads.Length) * 100.0 / LogicalCount;
    public double Duty => Volatile.Read(ref duty);
    public void Pause() => Volatile.Write(ref duty, 0);
    public void Configure(int initial, double target, double baseline)
    {
        if (target == 0) { Volatile.Write(ref duty, 0); return; }
        int required = RequiredCores(cores, target - baseline);
        Expand(Math.Max(Math.Clamp(initial, 1, cores.Length), required));
        Volatile.Write(ref duty, Math.Clamp((target - baseline) / Capacity, 0, 1));
    }
    internal static int RequiredCores(PhysicalCore[] topology, double additional)
    {
        int required = 1, logical = topology.Sum(c => c.Threads.Length);
        while (required < topology.Length && topology.Take(required).Sum(c => c.Threads.Length) * 100.0 / logical < additional) required++;
        return required;
    }
    public void Adjust(double target, double actual, double? rawActual = null)
    {
        if (failure is not null) throw new InvalidOperationException("Error de afinidad o trabajador CPU.", failure);
        if (target == 0) { Volatile.Write(ref duty, 0); return; }
        if (Duty > .95 && actual < target - 5 && active < cores.Length)
        {
            int count = active;
            double missing = target - actual;
            while (count < cores.Length && cores.Skip(active).Take(count - active).Sum(c => c.Threads.Length) * 100.0 / LogicalCount < missing) count++;
            Expand(count);
        }
        Volatile.Write(ref duty, Feedback.Next(Duty, target, actual, Capacity, rawActual));
    }
    private void Expand(int count)
    {
        for (int index = active; index < count; index++)
            foreach (var cpu in cores[index].Threads)
            {
                var thread = new Thread(() => Burn(cpu)) { IsBackground = true, Priority = ThreadPriority.BelowNormal, Name = $"CPU {cpu.Group}:{cpu.Index}" };
                workers.Add(thread); thread.Start();
            }
        active = count;
    }
    private void Burn(LogicalCpu cpu)
    {
        try
        {
            Topology.Pin(cpu);
            ulong value = (ulong)cpu.Index + 1234567;
            var timer = Stopwatch.StartNew();
            while (!cancellation.IsCancellationRequested)
            {
                double start = timer.Elapsed.TotalMilliseconds;
                double stop = start + Duty * 100;
                while (!cancellation.IsCancellationRequested && timer.Elapsed.TotalMilliseconds < stop)
                {
                    for (int i = 0; i < 512; i++) { value ^= value << 13; value ^= value >> 7; value ^= value << 17; }
                    if (Duty == 0) break;
                }
                double remaining = start + 100 - timer.Elapsed.TotalMilliseconds;
                if (remaining > 0) cancellation.Token.WaitHandle.WaitOne((int)Math.Ceiling(remaining));
            }
            GC.KeepAlive(value);
        }
        catch (Exception ex) { failure = ex; }
    }
    public void Dispose()
    {
        Volatile.Write(ref duty, 0); cancellation.Cancel();
        foreach (var worker in workers) if (!worker.Join(1000)) throw new TimeoutException("El trabajador CPU no se detuvo.");
        cancellation.Dispose();
    }
}

internal static class Feedback
{
    public static double? ExternalCpu(double? total, double? own) => total is not null && own is not null ? Math.Max(0, total.Value - own.Value) : null;
    public static double Next(double duty, double target, double actual, double capacity = 100, double? rawActual = null) =>
        // The short lead term counters the moving average's delay during external load changes.
        target == 0 ? 0 : Math.Clamp(duty + (.2 * (target - actual) + .3 * (actual - (rawActual ?? actual))) / Math.Max(1, capacity), 0, 1);
}
