using LibreHardwareMonitor.Hardware;
using LibreHardwareMonitor.PawnIo;
using System.Security.Principal;

namespace PatiaHardwareHost;

internal static class SensorProvider
{
    private static Computer? computer;
    private static int refresh;
    public static void Refresh() => Interlocked.Exchange(ref refresh, 1);
    public static ProviderData Collect()
    {
        var result = ProviderData.Empty();
        if (Interlocked.Exchange(ref refresh, 0) != 0) Close();
        var capability = new Dictionary<string, Field>
        {
            ["pawnio_installed"] = Values.Known(PawnIo.IsInstalled, source: "PawnIO"),
            ["pawnio_version"] = Values.Known(PawnIo.Version?.ToString(), source: "PawnIO"),
            ["administrator"] = Values.Known(new WindowsPrincipal(WindowsIdentity.GetCurrent()).IsInRole(WindowsBuiltInRole.Administrator))
        };
        result.Devices.Add(new("capabilities", "capabilities", "Acceso al hardware", capability));
        if (!PawnIo.IsInstalled) result.Errors.Add(new("sensors", "driver_missing", "PawnIO no está instalado. Algunos sensores requieren la preparación inicial."));
        else if (PawnIo.Version < new Version(2, 2)) result.Errors.Add(new("sensors", "driver_version", "Se requiere PawnIO 2.2 o posterior para los módulos integrados."));
        if (computer is null)
        {
            computer = new Computer
            {
                IsCpuEnabled = true, IsGpuEnabled = true, IsMemoryEnabled = true,
                IsMotherboardEnabled = true, IsStorageEnabled = false, IsControllerEnabled = false,
                IsNetworkEnabled = false, IsBatteryEnabled = false
            };
            try { computer.Open(); }
            catch { computer = null; throw; }
        }
        foreach (IHardware hardware in computer.Hardware.ToArray()) Visit(hardware);
        return result;

        void Visit(IHardware hardware)
        {
            string id = "lhm:" + hardware.Identifier;
            string kind = hardware.HardwareType.ToString() switch
            {
                "Cpu" => "cpu", "GpuNvidia" or "GpuAmd" or "GpuIntel" => "gpu",
                "Memory" => "memory", "Motherboard" or "SuperIO" => "board", _ => "sensor_hardware"
            };
            var fields = new Dictionary<string, Field>();
            foreach (var property in hardware.Properties) fields[property.Key] = Values.Known(property.Value, source: "LibreHardwareMonitor");
            result.Devices.Add(new(id, "sensor_" + kind, hardware.Name, fields));
            try
            {
                hardware.Update();
                foreach (ISensor sensor in hardware.Sensors)
                {
                    string unit = sensor.SensorType.ToString() switch
                    {
                        "Temperature" => "°C", "Voltage" => "V", "Clock" => "MHz", "Frequency" => "Hz",
                        "Load" or "Control" or "Level" => "%", "Fan" => "RPM", "Power" => "W",
                        "Data" => "GiB", "SmallData" => "MiB", "Throughput" => "B/s", "Timing" => "ns",
                        "Current" => "A", "Energy" => "mWh", "TimeSpan" => "s", _ => sensor.SensorType.ToString()
                    };
                    double? value = sensor.Value is float v && float.IsFinite(v) ? v : null;
                    result.Readings.Add(new("lhm:" + sensor.Identifier, id, sensor.Name, value, unit, "LibreHardwareMonitor",
                        DateTimeOffset.UtcNow, value is null ? "unavailable" : "available", value is null ? Values.Unavailable : null));
                    if (sensor.SensorType.ToString() == "Timing") fields["SPD: " + sensor.Name] = Values.Known(value, unit, "SPD (perfil nominal)");
                }
            }
            catch (Exception ex) { result.Errors.Add(new("sensors", "hardware_failed", hardware.Name + ": " + ex.Message)); }
            foreach (IHardware child in hardware.SubHardware) Visit(child);
        }
    }
    public static void Close() { computer?.Close(); computer = null; }
}
