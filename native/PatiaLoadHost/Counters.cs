using System.Runtime.InteropServices;
using System.Text.RegularExpressions;

namespace PatiaLoadHost;

internal sealed class Counters : IDisposable
{
    private IntPtr query, cpu, gpu;
    public bool CpuAvailable => cpu != IntPtr.Zero;
    public bool GpuAvailable => gpu != IntPtr.Zero;
    [StructLayout(LayoutKind.Explicit, Size = 16)]
    private struct Value { [FieldOffset(0)] public uint Status; [FieldOffset(8)] public double Number; }
    [StructLayout(LayoutKind.Sequential)] private struct Item { public IntPtr Name; public Value Value; }
    [DllImport("pdh.dll", CharSet = CharSet.Unicode)] private static extern uint PdhOpenQueryW(string? source, UIntPtr user, out IntPtr query);
    [DllImport("pdh.dll", CharSet = CharSet.Unicode)] private static extern uint PdhAddEnglishCounterW(IntPtr query, string path, UIntPtr user, out IntPtr counter);
    [DllImport("pdh.dll")] private static extern uint PdhCollectQueryData(IntPtr query);
    [DllImport("pdh.dll")] private static extern uint PdhGetFormattedCounterValue(IntPtr counter, uint format, IntPtr type, out Value value);
    [DllImport("pdh.dll", CharSet = CharSet.Unicode)] private static extern uint PdhGetFormattedCounterArrayW(IntPtr counter, uint format, ref uint size, out uint count, IntPtr items);
    [DllImport("pdh.dll")] private static extern uint PdhCloseQuery(IntPtr query);
    public Counters()
    {
        if (PdhOpenQueryW(null, UIntPtr.Zero, out query) != 0) return;
        if (PdhAddEnglishCounterW(query, @"\Processor Information(_Total)\% Processor Time", UIntPtr.Zero, out cpu) != 0) cpu = IntPtr.Zero;
        if (PdhAddEnglishCounterW(query, @"\GPU Engine(*)\Utilization Percentage", UIntPtr.Zero, out gpu) != 0) gpu = IntPtr.Zero;
        PdhCollectQueryData(query);
    }
    public (double? Cpu, double? Gpu) Sample(string? luid)
    {
        if (query == IntPtr.Zero || PdhCollectQueryData(query) != 0) return (null, null);
        double? cpuValue = cpu != IntPtr.Zero && PdhGetFormattedCounterValue(cpu, 0x200, IntPtr.Zero, out var value) == 0 && value.Status is 0 or 1
            ? Math.Clamp(value.Number, 0, 100) : null;
        return (cpuValue, Gpu(luid));
    }
    private double? Gpu(string? luid)
    {
        if (gpu == IntPtr.Zero || luid is null) return null;
        uint size = 0;
        PdhGetFormattedCounterArrayW(gpu, 0x200, ref size, out _, IntPtr.Zero);
        if (size == 0) return null;
        IntPtr buffer = Marshal.AllocHGlobal(checked((int)size));
        try
        {
            if (PdhGetFormattedCounterArrayW(gpu, 0x200, ref size, out uint count, buffer) != 0) return null;
            var values = new List<(string Name, double Number)>();
            for (int i = 0; i < count; i++)
            {
                var item = Marshal.PtrToStructure<Item>(buffer + i * Marshal.SizeOf<Item>());
                if (item.Value.Status is not (0 or 1)) continue;
                values.Add((Marshal.PtrToStringUni(item.Name) ?? "", item.Value.Number));
            }
            return Aggregate(values, luid);
        }
        finally { Marshal.FreeHGlobal(buffer); }
    }
    internal static double? Aggregate(IEnumerable<(string Name, double Number)> values, string luid)
    {
            var engines = new Dictionary<string, double>();
            foreach (var (name, number) in values)
            {
                if (!double.IsFinite(number) || number < 0) continue;
                var match = Regex.Match(name, @"luid_0x([0-9a-f]+)_0x([0-9a-f]+)_phys_(\d+)_eng_(\d+)", RegexOptions.IgnoreCase);
                if (!match.Success) continue;
                ulong id = (Convert.ToUInt64(match.Groups[1].Value, 16) << 32) | Convert.ToUInt64(match.Groups[2].Value, 16);
                if (!string.Equals(id.ToString("X"), luid, StringComparison.OrdinalIgnoreCase)) continue;
                string key = match.Groups[3].Value + ":" + match.Groups[4].Value;
                engines[key] = engines.GetValueOrDefault(key) + number;
            }
            return engines.Count == 0 ? null : Math.Clamp(engines.Values.Max(), 0, 100);
    }
    public void Dispose() { if (query != IntPtr.Zero) PdhCloseQuery(query); query = IntPtr.Zero; }
}
