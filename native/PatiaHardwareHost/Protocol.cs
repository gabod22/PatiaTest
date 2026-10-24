using System.Text.Json.Serialization;

namespace PatiaHardwareHost;

public record Field(object? Value, string? Unit = null, string Source = "Windows", string? Reason = null)
{
    public string Availability { get; init; } = Value is null ? "unavailable" : "available";
}

public record Device(string Id, string Kind, string Name, Dictionary<string, Field> Fields);
public record Reading(string Id, string DeviceId, string Name, double? Value, string Unit,
    string Source, DateTimeOffset Timestamp, string Availability = "available", string? Reason = null);
public record ProviderError(string Provider, string Code, string Message);
public record ProviderData(List<Device> Devices, List<Reading> Readings, List<ProviderError> Errors)
{
    public static ProviderData Empty() => new([], [], []);
}
public record Request(int Version, string Id, string Operation);
public record Response(int Version, string Id, string Operation, DateTimeOffset Timestamp,
    List<Device> Devices, List<Reading> Readings, List<ProviderError> Errors);

public static class Values
{
    public const string Unavailable = "El dispositivo o su controlador no expone este dato.";
    public static Field Known(object? value, string? unit = null, string source = "Windows") =>
        new(value, unit, source, value is null ? Unavailable : null);
    public static Field Missing(string reason = Unavailable, string? unit = null) => new(null, unit, Reason: reason);
    public static double? BatteryHealth(uint full, uint design, bool relative) =>
        relative || full == uint.MaxValue || design == uint.MaxValue || full == 0 || design == 0
            ? null : 100.0 * full / design;
}
