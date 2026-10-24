// Read-only interop with installed vendor drivers. No vendor DLL is redistributed.
// API references: NVIDIA NVML and AMD ADL SDK (see docs/HARDWARE.md).
using System.Runtime.InteropServices;
using System.Text;

namespace PatiaHardwareHost;

internal static class VendorGpuDetails
{
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int NoArgs();
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int Count(out uint count);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int Handle(uint index, out IntPtr device);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int StringQuery(IntPtr device, StringBuilder value, uint size);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int UIntQuery(IntPtr device, out uint value);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int ClockQuery(IntPtr device, uint clock, out uint value);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int PciQuery(IntPtr device, out PciInfo info);
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    private struct PciInfo
    {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 16)] public string Legacy;
        public uint Domain, Bus, Device, DeviceId, Subsystem;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string BusId;
    }
    private static T? Get<T>(IntPtr library, string name) where T : Delegate =>
        NativeLibrary.TryGetExport(library, name, out IntPtr address) ? Marshal.GetDelegateForFunctionPointer<T>(address) : null;

    public static void Enrich(ProviderData result)
    {
        try { Nvidia(result); }
        catch (Exception ex) { result.Errors.Add(new("gpu", "nvml_failed", ex.Message)); }
        try { Amd(result); }
        catch (Exception ex) { result.Errors.Add(new("gpu", "adl_failed", ex.Message)); }
    }
    private static void Nvidia(ProviderData result)
    {
        if (!NativeLibrary.TryLoad(Path.Combine(Environment.SystemDirectory, "nvml.dll"), out var library)) return;
        bool initialized = false;
        try
        {
            var init = Get<NoArgs>(library, "nvmlInit_v2");
            if (init is null || init() != 0) return;
            initialized = true;
            var count = Get<Count>(library, "nvmlDeviceGetCount_v2");
            var handle = Get<Handle>(library, "nvmlDeviceGetHandleByIndex_v2");
            if (count is null || handle is null || count(out uint total) != 0) return;
            for (uint i = 0; i < total; i++)
            {
                if (handle(i, out IntPtr gpu) != 0) continue;
                string? Text(string function)
                {
                    var query = Get<StringQuery>(library, function); var value = new StringBuilder(256);
                    return query is not null && query(gpu, value, 256) == 0 ? value.ToString() : null;
                }
                string name = Text("nvmlDeviceGetName") ?? "NVIDIA GPU";
                string identity = Text("nvmlDeviceGetUUID") ?? i.ToString();
                var fields = new Dictionary<string, Field>();
                Device? match = null;
                var pci = Get<PciQuery>(library, "nvmlDeviceGetPciInfo_v3");
                if (pci is not null && pci(gpu, out var info) == 0)
                {
                    fields["pci_bus_id"] = Values.Known(info.BusId, source: "NVML");
                    string device = (info.DeviceId >> 16).ToString("X4");
                    var matches = result.Devices.Where(d => d.Fields.GetValueOrDefault("pci_vendor")?.Value?.ToString() == "10DE"
                        && d.Fields.GetValueOrDefault("pci_device")?.Value?.ToString() == device
                        && d.Fields.GetValueOrDefault("pci_subsystem")?.Value?.ToString() == info.Subsystem.ToString("X8")).ToList();
                    if (matches.Count == 1) match = matches[0]; // Never guess between identical GPUs.
                }
                fields["uuid"] = Values.Known(identity, source: "NVML");
                fields["vbios"] = Values.Known(Text("nvmlDeviceGetVbiosVersion"), source: "NVML");
                foreach (var (key, function, unit) in new[] { ("pcie_generation", "nvmlDeviceGetCurrPcieLinkGeneration", ""),
                    ("pcie_width", "nvmlDeviceGetCurrPcieLinkWidth", "lanes"), ("memory_bus_width", "nvmlDeviceGetMemoryBusWidth", "bit"),
                    ("gpu_cores", "nvmlDeviceGetNumGpuCores", ""), ("architecture_code", "nvmlDeviceGetArchitecture", "") })
                {
                    var query = Get<UIntQuery>(library, function);
                    fields[key] = query is not null && query(gpu, out uint value) == 0 ? Values.Known(value, unit, "NVML") : Values.Missing();
                }
                var clock = Get<ClockQuery>(library, "nvmlDeviceGetMaxClockInfo");
                foreach (var (key, type) in new[] { ("max_gpu_clock", 0u), ("max_memory_clock", 2u) })
                    fields[key] = clock is not null && clock(gpu, type, out uint value) == 0 ? Values.Known(value, "MHz", "NVML (máximo reportado)") : Values.Missing();
                if (match is not null) foreach (var f in fields) match.Fields[f.Key] = f.Value;
                else result.Devices.Add(new("gpu:nvml:" + identity, "gpu_vendor", name + " (NVML)", fields));
            }
        }
        finally
        {
            if (initialized) Get<NoArgs>(library, "nvmlShutdown")?.Invoke();
            NativeLibrary.Free(library);
        }
    }

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate IntPtr Allocate(int size);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int Create(Allocate allocate, int connected, out IntPtr context);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int Destroy(IntPtr context);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int AdapterCount(IntPtr context, out int count);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int Adapters(IntPtr context, IntPtr adapters, int size);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int MemoryQuery(IntPtr context, int index, out MemoryInfo memory);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int BiosQuery(IntPtr context, int index, out BiosInfo bios);
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    private struct Adapter
    {
        public int Size, Index;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Udid;
        public int Bus, Device, Function, Vendor;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Name;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Display;
        public int Present, Exists;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Driver;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string DriverExt;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Pnp;
        public int OsDisplayIndex;
    }
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    private struct MemoryInfo
    {
        public long Size;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Type;
        public long Bandwidth;
    }
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    private struct BiosInfo
    {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Part;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Version;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string Date;
    }
    private static void Amd(ProviderData result)
    {
        if (!NativeLibrary.TryLoad(Path.Combine(Environment.SystemDirectory, "atiadlxx.dll"), out var library)) return;
        IntPtr context = IntPtr.Zero;
        Allocate allocator = Marshal.AllocHGlobal;
        try
        {
            var create = Get<Create>(library, "ADL2_Main_Control_Create");
            if (create is null || create(allocator, 1, out context) != 0) return;
            var count = Get<AdapterCount>(library, "ADL2_Adapter_NumberOfAdapters_Get");
            var enumerate = Get<Adapters>(library, "ADL2_Adapter_AdapterInfo_Get");
            if (count is null || enumerate is null || count(context, out int total) != 0 || total < 0 || total > 256) return;
            int size = Marshal.SizeOf<Adapter>();
            IntPtr buffer = Marshal.AllocHGlobal(total * size);
            try
            {
                for (int i = 0; i < total; i++) Marshal.WriteInt32(buffer + i * size, size);
                if (enumerate(context, buffer, total * size) != 0) return;
                var seen = new HashSet<string>();
                for (int i = 0; i < total; i++)
                {
                    var adapter = Marshal.PtrToStructure<Adapter>(buffer + i * size);
                    if (adapter.Present == 0 || adapter.Vendor != 1002 || !seen.Add(adapter.Pnp)) continue;
                    var match = result.Devices.FirstOrDefault(d => string.Equals(d.Fields.GetValueOrDefault("pnp_id")?.Value?.ToString(), adapter.Pnp, StringComparison.OrdinalIgnoreCase));
                    var fields = match?.Fields ?? new Dictionary<string, Field>();
                    fields["pci_bus"] = Values.Known(adapter.Bus, source: "AMD ADL");
                    fields["pci_device_number"] = Values.Known(adapter.Device, source: "AMD ADL");
                    var memory = Get<MemoryQuery>(library, "ADL2_Adapter_MemoryInfo_Get");
                    if (memory is not null && memory(context, adapter.Index, out var mem) == 0)
                    {
                        fields["memory_type"] = Values.Known(mem.Type, source: "AMD ADL");
                        fields["dedicated_memory"] = Values.Known(mem.Size, "B", "AMD ADL");
                        fields["memory_bandwidth"] = Values.Known(mem.Bandwidth, "MB/s", "AMD ADL");
                    }
                    var bios = Get<BiosQuery>(library, "ADL2_Adapter_VideoBiosInfo_Get");
                    if (bios is not null && bios(context, adapter.Index, out var b) == 0)
                    {
                        fields["vbios"] = Values.Known(b.Version, source: "AMD ADL");
                        fields["vbios_date"] = Values.Known(b.Date, source: "AMD ADL");
                    }
                    if (match is null) result.Devices.Add(new("gpu:adl:" + adapter.Pnp.ToLowerInvariant(), "gpu_vendor", adapter.Name + " (ADL)", fields));
                }
            }
            finally { Marshal.FreeHGlobal(buffer); }
        }
        finally
        {
            if (context != IntPtr.Zero) Get<Destroy>(library, "ADL2_Main_Control_Destroy")?.Invoke(context);
            GC.KeepAlive(allocator);
            NativeLibrary.Free(library);
        }
    }
}
