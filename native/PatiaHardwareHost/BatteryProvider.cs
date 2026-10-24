using System.ComponentModel;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;

namespace PatiaHardwareHost;

internal static class BatteryProvider
{
    private static readonly Guid BatteryGuid = new("72631e54-78a4-11d0-bcf7-00aa00b7b32a");
    private const uint Unknown = uint.MaxValue;
    [StructLayout(LayoutKind.Sequential)]
    private struct InterfaceData { public int Size; public Guid Guid; public uint Flags; public UIntPtr Reserved; }
    [StructLayout(LayoutKind.Sequential)]
    private struct Query { public uint Tag; public int Level; public int Rate; }
    [StructLayout(LayoutKind.Sequential)]
    private struct Info
    {
        public uint Capabilities; public byte Technology;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 3)] public byte[] Reserved;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4)] public byte[] Chemistry;
        public uint Design, Full, Alert1, Alert2, Bias, Cycles;
    }
    [StructLayout(LayoutKind.Sequential)]
    private struct Wait { public uint Tag, Timeout, State, Low, High; }
    [StructLayout(LayoutKind.Sequential)]
    private struct Status { public uint State, Capacity, Voltage; public int Rate; }
    [DllImport("setupapi.dll", SetLastError = true)]
    private static extern IntPtr SetupDiGetClassDevsW(ref Guid guid, IntPtr enumerator, IntPtr parent, uint flags);
    [DllImport("setupapi.dll", SetLastError = true)]
    private static extern bool SetupDiEnumDeviceInterfaces(IntPtr set, IntPtr device, ref Guid guid, uint index, ref InterfaceData data);
    [DllImport("setupapi.dll", SetLastError = true)]
    private static extern bool SetupDiGetDeviceInterfaceDetailW(IntPtr set, ref InterfaceData data, IntPtr detail, uint size, out uint needed, IntPtr device);
    [DllImport("setupapi.dll")]
    private static extern bool SetupDiDestroyDeviceInfoList(IntPtr set);
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern SafeFileHandle CreateFileW(string name, uint access, uint share, IntPtr security, uint creation, uint flags, IntPtr template);
    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool DeviceIoControl(SafeFileHandle handle, uint code, byte[] input, int inputSize,
        byte[] output, int outputSize, out int returned, IntPtr overlapped);

    private static byte[] Bytes<T>(T value) where T : struct
    {
        int size = Marshal.SizeOf<T>();
        IntPtr ptr = Marshal.AllocHGlobal(size);
        try { Marshal.StructureToPtr(value, ptr, false); byte[] bytes = new byte[size]; Marshal.Copy(ptr, bytes, 0, size); return bytes; }
        finally { Marshal.FreeHGlobal(ptr); }
    }
    private static T Struct<T>(byte[] bytes) where T : struct
    {
        var pin = GCHandle.Alloc(bytes, GCHandleType.Pinned);
        try { return Marshal.PtrToStructure<T>(pin.AddrOfPinnedObject()); }
        finally { pin.Free(); }
    }
    private static byte[] Io(SafeFileHandle handle, uint code, byte[] input, int size)
    {
        byte[] output = new byte[size];
        if (!DeviceIoControl(handle, code, input, input.Length, output, size, out int returned, IntPtr.Zero))
            throw new Win32Exception(Marshal.GetLastWin32Error());
        if (returned < size && size != 4096) throw new InvalidDataException("Respuesta de batería incompleta.");
        return output;
    }
    public static ProviderData Collect()
    {
        ProviderData result = ProviderData.Empty();
        Guid guid = BatteryGuid;
        IntPtr set = SetupDiGetClassDevsW(ref guid, IntPtr.Zero, IntPtr.Zero, 0x12);
        if (set == new IntPtr(-1)) throw new Win32Exception(Marshal.GetLastWin32Error());
        try
        {
            for (uint index = 0; ; index++)
            {
                var data = new InterfaceData { Size = Marshal.SizeOf<InterfaceData>() };
                if (!SetupDiEnumDeviceInterfaces(set, IntPtr.Zero, ref guid, index, ref data))
                {
                    int error = Marshal.GetLastWin32Error();
                    if (error != 259) result.Errors.Add(new("battery", error.ToString(), new Win32Exception(error).Message));
                    break;
                }
                SetupDiGetDeviceInterfaceDetailW(set, ref data, IntPtr.Zero, 0, out uint needed, IntPtr.Zero);
                IntPtr detail = Marshal.AllocHGlobal(checked((int)needed));
                try
                {
                    Marshal.WriteInt32(detail, IntPtr.Size == 8 ? 8 : 6);
                    if (!SetupDiGetDeviceInterfaceDetailW(set, ref data, detail, needed, out _, IntPtr.Zero))
                        throw new Win32Exception(Marshal.GetLastWin32Error());
                    string path = Marshal.PtrToStringUni(detail + 4)!;
                    var fields = new Dictionary<string, Field>();
                    var device = new Device("battery:" + path.ToLowerInvariant(), "battery", $"Batería {index + 1}", fields);
                    result.Devices.Add(device);
                    try { Read(device, path, result); }
                    catch (Exception ex)
                    {
                        fields["status"] = Values.Missing(ex.Message);
                        result.Errors.Add(new("battery", "query_failed", ex.Message));
                    }
                }
                finally { Marshal.FreeHGlobal(detail); }
            }
        }
        finally { SetupDiDestroyDeviceInfoList(set); }
        return result;
    }
    private static void Read(Device device, string path, ProviderData result)
    {
        using var handle = CreateFileW(path, 0xC0000000, 3, IntPtr.Zero, 3, 0, IntPtr.Zero);
        if (handle.IsInvalid) throw new Win32Exception(Marshal.GetLastWin32Error());
        uint tag = BitConverter.ToUInt32(Io(handle, 0x294040, BitConverter.GetBytes(0u), 4));
        if (tag == 0) throw new IOException("Batería retirada o sin etiqueta válida.");
        byte[] QueryBytes(int level) => Bytes(new Query { Tag = tag, Level = level });
        var info = Struct<Info>(Io(handle, 0x294044, QueryBytes(0), Marshal.SizeOf<Info>()));
        bool relative = (info.Capabilities & 0x40000000) != 0;
        string capacityUnit = relative ? "relative" : "mWh";
        var f = device.Fields;
        void Number(string key, uint value, string? unit = null) => f[key] = Values.Known(value == Unknown ? null : value, unit, "Battery IOCTL");
        void Optional(string key, int level, Func<byte[], object?> convert, int size = 4, string? unit = null)
        {
            try { f[key] = Values.Known(convert(Io(handle, 0x294044, QueryBytes(level), size)), unit, "Battery IOCTL"); }
            catch (Exception ex) { f[key] = Values.Missing(ex.Message, unit); }
        }
        foreach (var (key, level) in new[] { ("name", 4), ("manufacturer", 6), ("serial", 8), ("unique_id", 7) })
            Optional(key, level, b => System.Text.Encoding.Unicode.GetString(b).TrimEnd('\0'), 4096);
        Optional("manufacture_date", 5, b => b[0] == 0 || b[1] == 0 ? null : new DateTime(BitConverter.ToUInt16(b, 2), b[1], b[0]).ToString("yyyy-MM-dd"));
        f["chemistry"] = Values.Known(System.Text.Encoding.ASCII.GetString(info.Chemistry).TrimEnd('\0'), source: "Battery IOCTL");
        f["relative_capacity"] = Values.Known(relative, source: "Battery IOCTL");
        Number("design_capacity", info.Design, capacityUnit); Number("full_capacity", info.Full, capacityUnit);
        f["health"] = Values.Known(Values.BatteryHealth(info.Full, info.Design, relative), "%", "full_capacity / design_capacity");
        f["cycles"] = Values.Known(info.Cycles == 0 || info.Cycles == Unknown ? null : info.Cycles, source: "Battery IOCTL");
        Optional("temperature", 2, b => BitConverter.ToUInt32(b) is 0 or Unknown ? null : BitConverter.ToUInt32(b) / 10.0 - 273.15, unit: "°C");
        Optional("remaining_time", 3, b => BitConverter.ToUInt32(b) == Unknown ? null : BitConverter.ToUInt32(b), unit: "s");
        try
        {
            var status = Struct<Status>(Io(handle, 0x29404c, Bytes(new Wait { Tag = tag }), Marshal.SizeOf<Status>()));
            Number("current_capacity", status.Capacity, capacityUnit); Number("voltage", status.Voltage, "mV");
            f["rate"] = Values.Known(status.Rate == int.MinValue ? null : status.Rate, relative ? "relative/h" : "mW", "Battery IOCTL");
            f["charge"] = Values.Known(status.Capacity == Unknown || info.Full is 0 or Unknown ? null : 100.0 * status.Capacity / info.Full, "%", "Battery IOCTL");
            f["power_state"] = Values.Known((status.State & 2) != 0 ? "Descargando" : (status.State & 4) != 0 ? "Cargando" : (status.State & 1) != 0 ? "Conectada" : "En batería", source: "Battery IOCTL");
        }
        catch (Exception ex) { result.Errors.Add(new("battery", "status_failed", ex.Message)); }
        DateTimeOffset now = DateTimeOffset.UtcNow;
        foreach (string key in new[] { "charge", "voltage", "rate", "temperature" })
            if (f.TryGetValue(key, out Field? field) && field.Value is not null)
                result.Readings.Add(new(device.Id + ":" + key, device.Id, key, Convert.ToDouble(field.Value), field.Unit ?? "", field.Source, now));
    }
}
