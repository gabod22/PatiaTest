using System.Globalization;
using System.Numerics;
using DiskInfoToolkit;

namespace PatiaHardwareHost;

internal static class StorageProvider
{
    public static BigInteger Raw(SmartAttribute attribute) => new(attribute.Attribute.RawValue, isUnsigned: true, isBigEndian: false);
    public static BigInteger NvmeBytes(BigInteger dataUnits) => dataUnits * 512000;
    public static int NvmeLife(int used) => Math.Max(0, 100 - used);
    public static Dictionary<string, Field> DecodeNvme(IReadOnlyList<SmartAttribute> attributes)
    {
        var fields = new Dictionary<string, Field>();
        void Add(string key, object? value, string? unit = null) => fields[key] = Values.Known(value, unit, "NVMe SMART");
        void Counter(string type, string key, string? unit = null, bool bytes = false)
        {
            var attr = attributes.FirstOrDefault(a => a.Info.Type.ToString() == type);
            if (attr is not null) Add(key, (bytes ? NvmeBytes(Raw(attr)) : Raw(attr)).ToString(CultureInfo.InvariantCulture), unit);
        }
        Counter("HostDataRead", "host_reads", "B", true); Counter("HostDataWritten", "host_writes", "B", true);
        Counter("PowerCycleCount", "power_on_count"); Counter("PowerOnHours", "power_on_hours", "h");
        Counter("MediaAndDataIntegrityErrors", "media_errors"); Counter("UnsafeShutdownCount", "unsafe_shutdowns");
        var used = attributes.FirstOrDefault(a => a.Info.Type.ToString() == "PercentageUsed");
        if (used is not null)
        {
            int percentage = (int)Raw(used);
            Add("percentage_used", percentage, "%"); Add("life_remaining", NvmeLife(percentage), "%");
            Add("life_calculation", "max(0, 100 - percentage_used); estimación de desgaste NVMe");
        }
        var warning = attributes.FirstOrDefault(a => a.Info.Type.ToString() == "CriticalWarning");
        if (warning is not null)
        {
            int flags = (int)Raw(warning);
            Add("critical_warning", flags);
            Add("health_status", flags == 0 ? "Sin advertencias críticas" : (flags & 12) != 0 ? "Malo" : "Precaución");
        }
        return fields;
    }
    public static ProviderData Collect()
    {
        var result = ProviderData.Empty();
        StorageManager.ReloadStorages();
        foreach (var storage in StorageManager.Storages.ToArray())
        {
            string id = WindowsInventory.DiskId(storage.DeviceID, @"\\.\PHYSICALDRIVE" + storage.DriveNumber);
            var f = new Dictionary<string, Field>();
            var device = new Device(id, "disk", storage.Model, f);
            result.Devices.Add(device);
            void Add(string key, object? value, string? unit = null) => f[key] = Values.Known(value, unit, "DiskInfoToolkit");
            Add("model", storage.Model); Add("serial", storage.SerialNumber); Add("firmware", storage.FirmwareRev);
            Add("capacity", storage.TotalSize, "B"); Add("interface", storage.BusType.ToString());
            Add("path", @"\\.\PHYSICALDRIVE" + storage.DriveNumber); Add("pnp_id", storage.DeviceID); Add("drive_number", storage.DriveNumber);
            Add("controller", storage.StorageController); Add("is_ssd", storage.IsSSD); Add("is_nvme", storage.IsNVMe);
            foreach (string key in new[] { "health_status", "life_remaining", "percentage_used", "temperature", "host_reads", "host_writes", "power_on_hours", "power_on_count", "smart" })
                f[key] = Values.Missing("La unidad o su controladora no entrega este dato SMART.");
            try
            {
                storage.Update();
                var smart = storage.Smart;
                var attributes = smart.SmartAttributes.Where(a => a?.Info is not null).ToList();
                if (attributes.Count == 0) continue; // Library defaults are not measurements.
                Add("smart", attributes.Select(a => new
                {
                    id = a.Info.ID, type = a.Info.Type.ToString(), current = storage.IsNVMe ? (int?)null : a.Attribute.CurrentValue,
                    worst = storage.IsNVMe ? (int?)null : a.Attribute.WorstValue, threshold = storage.IsNVMe ? (int?)null : a.Attribute.Threshold,
                    raw_hex = Convert.ToHexString(a.Attribute.RawValue), raw_decimal = Raw(a).ToString(CultureInfo.InvariantCulture)
                }).ToList());
                Add("temperature", smart.Temperature, "°C");
                if (storage.IsNVMe)
                {
                    foreach (var field in DecodeNvme(attributes)) f[field.Key] = field.Value;
                }
                else
                {
                    if (smart.DiskStatus.ToString() != "Unknown") Add("health_status", smart.DiskStatus.ToString());
                    // Life is only meaningful for SSDs with a recognized vendor attribute.
                    if (storage.IsSSD && smart.Life is >= 0 and <= 100 && attributes.Any(a => a.Info.Type.ToString() == "RemainingLife")) Add("life_remaining", smart.Life, "%");
                    if (smart.HostReads is not null && smart.HostReads != 0) Add("host_reads", smart.HostReads, "GiB");
                    if (smart.HostWrites is not null && smart.HostWrites != 0) Add("host_writes", smart.HostWrites, "GiB");
                    if (storage.DetectedTimeUnitType.ToString() != "PowerOnUnknown" && attributes.Any(a => a.Info.Type.ToString() == "PowerOnHours")) Add("power_on_hours", smart.DetectedPowerOnHours, "h");
                    if (attributes.Any(a => a.Info.Type.ToString() == "PowerCycleCount")) Add("power_on_count", smart.PowerOnCount);
                }
                if (smart.Temperature is not null)
                    result.Readings.Add(new(id + ":temperature", id, "Temperatura del disco", smart.Temperature, "°C", "SMART", DateTimeOffset.UtcNow));
            }
            catch (Exception ex) { result.Errors.Add(new("storage", "query_failed", storage.Model + ": " + ex.Message)); }
        }
        return result;
    }
}
