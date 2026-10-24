using System.Management;
using System.Runtime.InteropServices;

namespace PatiaHardwareHost;

internal static class WindowsInventory
{
    public static string DiskId(string pnp, string path) => "disk:" + (string.IsNullOrWhiteSpace(pnp) ? path : pnp).ToLowerInvariant();
    public static List<Dictionary<string, object?>> Query(string query)
    {
        using var search = new ManagementObjectSearcher("root\\cimv2", query);
        search.Options.Timeout = TimeSpan.FromSeconds(4);
        using var rows = search.Get();
        var result = new List<Dictionary<string, object?>>();
        foreach (ManagementBaseObject row in rows)
        {
            using (row) result.Add(row.Properties.Cast<PropertyData>().ToDictionary(p => p.Name, p => (object?)p.Value, StringComparer.OrdinalIgnoreCase));
        }
        return result;
    }
    public static string Text(Dictionary<string, object?> row, string key) => row.GetValueOrDefault(key)?.ToString()?.Trim() ?? "";
    public static ProviderData Collect()
    {
        var result = ProviderData.Empty();
        AddClass("Win32_Processor", "cpu", "DeviceID", "Name", new()
        {
            ["name"] = ("Name", null), ["manufacturer"] = ("Manufacturer", null), ["socket"] = ("SocketDesignation", null),
            ["cores"] = ("NumberOfCores", null), ["threads"] = ("NumberOfLogicalProcessors", null), ["architecture"] = ("Architecture", null),
            ["max_clock"] = ("MaxClockSpeed", "MHz"), ["configured_clock"] = ("CurrentClockSpeed", "MHz"),
            ["l2_cache"] = ("L2CacheSize", "KiB"), ["l3_cache"] = ("L3CacheSize", "KiB"), ["processor_id"] = ("ProcessorId", null),
            ["family"] = ("Family", null), ["stepping"] = ("Stepping", null), ["revision"] = ("Revision", null)
        });
        AddClass("Win32_PhysicalMemory", "memory", "DeviceLocator", "DeviceLocator", new()
        {
            ["capacity"] = ("Capacity", "B"), ["type"] = ("SMBIOSMemoryType", null), ["manufacturer"] = ("Manufacturer", null),
            ["part_number"] = ("PartNumber", null), ["serial"] = ("SerialNumber", null), ["slot"] = ("DeviceLocator", null),
            ["bank"] = ("BankLabel", null), ["nominal_speed"] = ("Speed", "MT/s"), ["configured_speed"] = ("ConfiguredClockSpeed", "MT/s"),
            ["configured_voltage"] = ("ConfiguredVoltage", "mV"), ["data_width"] = ("DataWidth", "bit"), ["total_width"] = ("TotalWidth", "bit")
        });
        AddClass("Win32_BaseBoard", "board", "Tag", "Product", new()
        {
            ["manufacturer"] = ("Manufacturer", null), ["model"] = ("Product", null), ["revision"] = ("Version", null), ["serial"] = ("SerialNumber", null)
        });
        AddClass("Win32_BIOS", "bios", "Name", "Name", new()
        {
            ["manufacturer"] = ("Manufacturer", null), ["version"] = ("SMBIOSBIOSVersion", null),
            ["release_date"] = ("ReleaseDate", null), ["serial"] = ("SerialNumber", null)
        });
        return result;

        void AddClass(string cls, string kind, string id, string name, Dictionary<string, (string Property, string? Unit)> map)
        {
            try
            {
                foreach (var row in Query("SELECT * FROM " + cls))
                {
                    var fields = map.ToDictionary(k => k.Key, k => Values.Known(Clean(row.GetValueOrDefault(k.Value.Property)), k.Value.Unit, "WMI/SMBIOS"));
                    if (kind == "memory")
                    {
                        string type = row.GetValueOrDefault("SMBIOSMemoryType")?.ToString() ?? "0";
                        fields["type"] = Values.Known(type switch { "20" => "DDR", "21" => "DDR2", "24" => "DDR3", "26" => "DDR4", "34" => "DDR5", "30" => "LPDDR4", "35" => "LPDDR5", "0" => null, _ => "SMBIOS " + type }, source: "WMI/SMBIOS");
                    }
                    if (kind == "cpu") fields["architecture"] = Values.Known(row.GetValueOrDefault("Architecture")?.ToString() switch { "0" => "x86", "9" => "x64", "12" => "ARM64", _ => null }, source: "WMI");
                    if (kind == "memory") { fields["spd"] = Values.Missing("Los perfiles SPD solo están disponibles cuando el proveedor puede leer el módulo."); fields["timings"] = Values.Missing(); }
                    result.Devices.Add(new(kind + ":" + Text(row, id).ToLowerInvariant(), kind, Text(row, name), fields));
                }
            }
            catch (Exception ex) { result.Errors.Add(new(kind, "wmi_failed", ex.Message)); }
        }
    }
    private static object? Clean(object? value) => value is string text ? string.IsNullOrWhiteSpace(text) ? null : text.Trim() : value;
    public static ProviderData Disks()
    {
        var result = ProviderData.Empty();
        foreach (var row in Query("SELECT * FROM Win32_DiskDrive"))
        {
            var f = new Dictionary<string, Field>();
            foreach (var (key, property) in new[] { ("model", "Model"), ("serial", "SerialNumber"), ("firmware", "FirmwareRevision"),
                ("interface", "InterfaceType"), ("path", "DeviceID"), ("pnp_id", "PNPDeviceID"), ("drive_number", "Index") })
                f[key] = Values.Known(Clean(row.GetValueOrDefault(property)), source: "WMI");
            f["capacity"] = Values.Known(row.GetValueOrDefault("Size"), "B", "WMI");
            foreach (string key in new[] { "health_status", "life_remaining", "temperature", "host_reads", "host_writes", "power_on_hours", "power_on_count", "smart" })
                f[key] = Values.Missing("SMART no disponible: la unidad, los permisos o la controladora no permiten consultarlo.");
            try
            {
                string escaped = Text(row, "DeviceID").Replace("\\", "\\\\").Replace("'", "\\'");
                var volumes = new List<string>();
                foreach (var partition in Query($"ASSOCIATORS OF {{Win32_DiskDrive.DeviceID='{escaped}'}} WHERE AssocClass=Win32_DiskDriveToDiskPartition"))
                {
                    string part = Text(partition, "DeviceID").Replace("'", "\\'");
                    volumes.AddRange(Query($"ASSOCIATORS OF {{Win32_DiskPartition.DeviceID='{part}'}} WHERE AssocClass=Win32_LogicalDiskToPartition").Select(v => Text(v, "DeviceID")));
                }
                f["volumes"] = Values.Known(volumes, source: "WMI");
            }
            catch (Exception ex) { f["volumes"] = Values.Missing(ex.Message); }
            result.Devices.Add(new(DiskId(Text(row, "PNPDeviceID"), Text(row, "DeviceID")), "disk", Text(row, "Model"), f));
        }
        return result;
    }
}

internal static class GpuProvider
{
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    private struct Description
    {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)] public string Name;
        public uint Vendor, Device, Subsystem, Revision;
        public UIntPtr DedicatedVideo, DedicatedSystem, SharedSystem;
        public long Luid;
        public uint Flags;
    }
    [DllImport("dxgi.dll", PreserveSig = true)] private static extern int CreateDXGIFactory1(ref Guid iid, out IntPtr factory);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] private delegate int EnumAdapters(IntPtr factory, uint index, out IntPtr adapter);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] private delegate int GetDescription(IntPtr adapter, out Description desc);
    private static T Method<T>(IntPtr obj, int slot) where T : Delegate => Marshal.GetDelegateForFunctionPointer<T>(Marshal.ReadIntPtr(Marshal.ReadIntPtr(obj), slot * IntPtr.Size));
    public static ProviderData Collect()
    {
        var result = ProviderData.Empty();
        var rows = new List<Dictionary<string, object?>>();
        try { rows = WindowsInventory.Query("SELECT * FROM Win32_VideoController"); }
        catch (Exception ex) { result.Errors.Add(new("gpu", "wmi_failed", ex.Message)); }
        foreach (var row in rows)
        {
            var f = new Dictionary<string, Field>();
            foreach (var (key, property) in new[] { ("name", "Name"), ("manufacturer", "AdapterCompatibility"), ("pnp_id", "PNPDeviceID"),
                ("driver_version", "DriverVersion"), ("driver_date", "DriverDate"), ("video_processor", "VideoProcessor"), ("status", "Status") })
                f[key] = Values.Known(string.IsNullOrWhiteSpace(WindowsInventory.Text(row, property)) ? null : WindowsInventory.Text(row, property), source: "WMI");
            foreach (string key in new[] { "dedicated_memory", "shared_memory", "memory_type", "vbios", "pcie_link", "capabilities" }) f[key] = Values.Missing();
            result.Devices.Add(new("gpu:" + WindowsInventory.Text(row, "PNPDeviceID").ToLowerInvariant(), "gpu", WindowsInventory.Text(row, "Name"), f));
        }
        var used = new HashSet<string>();
        IntPtr factory = IntPtr.Zero;
        try
        {
            Guid guid = new("770aae78-f26f-4dba-a829-253c83d1b387");
            Marshal.ThrowExceptionForHR(CreateDXGIFactory1(ref guid, out factory));
            var enumerate = Method<EnumAdapters>(factory, 12);
            for (uint index = 0; ; index++)
            {
                int status = enumerate(factory, index, out IntPtr adapter);
                if (status == unchecked((int)0x887A0002)) break;
                Marshal.ThrowExceptionForHR(status);
                try
                {
                    Marshal.ThrowExceptionForHR(Method<GetDescription>(adapter, 10)(adapter, out var desc));
                    if ((desc.Flags & 2) != 0) continue; // Software adapters are not physical GPUs.
                    string match = $"VEN_{desc.Vendor:X4}&DEV_{desc.Device:X4}&SUBSYS_{desc.Subsystem:X8}";
                    Device? device = result.Devices.FirstOrDefault(d => !used.Contains(d.Id) && (d.Fields["pnp_id"].Value?.ToString()?.Contains(match, StringComparison.OrdinalIgnoreCase) ?? false));
                    if (device is null)
                    {
                        device = new("gpu:dxgi:" + desc.Luid.ToString("X"), "gpu", desc.Name, new());
                        result.Devices.Add(device);
                    }
                    used.Add(device.Id);
                    var f = device.Fields;
                    f["dedicated_memory"] = Values.Known(desc.DedicatedVideo.ToUInt64(), "B", "DXGI");
                    f["shared_memory"] = Values.Known(desc.SharedSystem.ToUInt64(), "B", "DXGI (máximo compartible)");
                    f["dedicated_system_memory"] = Values.Known(desc.DedicatedSystem.ToUInt64(), "B", "DXGI");
                    f["pci_vendor"] = Values.Known(desc.Vendor.ToString("X4"), source: "DXGI");
                    f["pci_device"] = Values.Known(desc.Device.ToString("X4"), source: "DXGI");
                    f["pci_subsystem"] = Values.Known(desc.Subsystem.ToString("X8"), source: "DXGI");
                    f["revision"] = Values.Known(desc.Revision, source: "DXGI");
                    f["adapter_luid"] = Values.Known(desc.Luid.ToString("X"), source: "DXGI");
                    if (!f.ContainsKey("manufacturer")) f["manufacturer"] = Values.Known(desc.Vendor switch { 0x10DE => "NVIDIA", 0x1002 => "AMD", 0x8086 => "Intel", _ => "PCI " + desc.Vendor.ToString("X4") }, source: "PCI vendor ID");
                }
                finally { Marshal.Release(adapter); }
            }
        }
        catch (Exception ex) { result.Errors.Add(new("gpu", "dxgi_failed", ex.Message)); }
        finally { if (factory != IntPtr.Zero) Marshal.Release(factory); }
        VendorGpuDetails.Enrich(result);
        foreach (var device in result.Devices)
            foreach (string key in new[] { "memory_type", "vbios", "pcie_link", "capabilities", "driver_version" })
                device.Fields.TryAdd(key, Values.Missing());
        return result;
    }
}
