using System.Numerics;
using DiskInfoToolkit;
using DiskInfoToolkit.Interop.Enums;
using DiskInfoToolkit.Interop.Structures;
using DiskInfoToolkit.Smart;

namespace PatiaHardwareHost;

internal static class SelfTests
{
    public static async Task Run(TextWriter output)
    {
        int checks = 0;
        void Check(bool condition, string message)
        {
            if (!condition) throw new Exception("Self-test failed: " + message);
            checks++;
        }
        Check(Values.BatteryHealth(60000, 50000, false) == 120, "health above 100 preserved");
        Check(Values.BatteryHealth(45000, 50000, false) == 90, "battery ratio");
        Check(Values.BatteryHealth(1, 0, false) is null, "zero design capacity");
        Check(Values.BatteryHealth(uint.MaxValue, 50000, false) is null, "unknown capacity sentinel");
        Check(Values.BatteryHealth(50000, 50000, true) is null, "relative capacities");
        SmartAttribute Attribute(SmartAttributeType type, BigInteger value)
        {
            byte[] raw = new byte[16];
            value.ToByteArray(isUnsigned: true).CopyTo(raw, 0);
            var info = (SmartAttributeInfo)Activator.CreateInstance(typeof(SmartAttributeInfo),
                System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic,
                null, [(byte)0, type, type.ToString()], null)!;
            return new SmartAttribute { Info = info, Attribute = new SmartAttributeStructure { RawValue = raw } };
        }
        var large = BigInteger.One << 80;
        var fields = StorageProvider.DecodeNvme([
            Attribute(SmartAttributeType.HostDataRead, large), Attribute(SmartAttributeType.HostDataWritten, 3),
            Attribute(SmartAttributeType.PercentageUsed, 150), Attribute(SmartAttributeType.CriticalWarning, 4),
            Attribute(SmartAttributeType.PowerOnHours, 0)]);
        Check(fields["host_reads"].Value?.ToString() == (large * 512000).ToString(), "128-bit NVMe counter without truncation");
        Check(fields["host_writes"].Value?.ToString() == "1536000" && fields["host_writes"].Unit == "B", "NVMe data unit conversion");
        Check((int)fields["percentage_used"].Value! == 150 && (int)fields["life_remaining"].Value! == 0, "wear above 100 retained");
        Check(fields["health_status"].Value?.ToString() == "Malo", "NVMe critical warning");
        Check(fields["power_on_hours"].Value?.ToString() == "0", "valid zero counter");
        Check(!StorageProvider.DecodeNvme([]).ContainsKey("health_status"), "missing log never means good");
        var slotCalls = 0;
        using var release = new ManualResetEventSlim(false);
        var blocked = new ProviderSlot("blocked", () => { Interlocked.Increment(ref slotCalls); release.Wait(); return ProviderData.Empty(); }, TimeSpan.Zero, 20);
        try
        {
            var first = await blocked.Get(false);
            var second = await blocked.Get(true);
            Check(first.Errors[0].Code == "timeout" && second.Errors[0].Code == "timeout" && slotCalls == 1, "blocked provider is not launched twice");
            var healthy = new ProviderSlot("healthy", () => ProviderData.Empty(), TimeSpan.Zero);
            Check((await healthy.Get(false)).Errors.Count == 0, "other providers remain available");
        }
        finally { release.Set(); }
        await Task.Delay(40);
        Check((await blocked.Get(false)).Errors.Count == 0, "provider recovery");
        await output.WriteLineAsync($"PASS: {checks} native checks");
    }
}
