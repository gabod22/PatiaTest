using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using PatiaHardwareHost;

Console.InputEncoding = Encoding.UTF8;
Console.OutputEncoding = new UTF8Encoding(false);
var output = Console.Out;
// Libraries must never write diagnostic text into the JSON protocol.
Console.SetOut(Console.Error);
var json = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
    PropertyNameCaseInsensitive = true,
    NumberHandling = JsonNumberHandling.AllowNamedFloatingPointLiterals
};
if (args.Contains("--self-test"))
{
    await SelfTests.Run(output);
    return;
}
var slots = new Dictionary<string, ProviderSlot>
{
    ["battery"] = new("battery", BatteryProvider.Collect, TimeSpan.FromSeconds(1)),
    ["inventory"] = new("inventory", WindowsInventory.Collect, TimeSpan.FromMinutes(5)),
    ["disk_inventory"] = new("disk_inventory", WindowsInventory.Disks, TimeSpan.FromSeconds(10)),
    ["gpu"] = new("gpu", GpuProvider.Collect, TimeSpan.FromSeconds(30)),
    ["storage"] = new("storage", StorageProvider.Collect, TimeSpan.FromSeconds(30)),
    ["sensors"] = new("sensors", SensorProvider.Collect, TimeSpan.FromSeconds(1))
};
while (await Console.In.ReadLineAsync() is { } line)
{
    Request? request = null;
    try
    {
        request = JsonSerializer.Deserialize<Request>(line, json) ?? throw new InvalidDataException("Solicitud vacía.");
        if (request.Version != 1) throw new InvalidDataException("Versión de protocolo no compatible.");
        if (request.Operation == "shutdown")
        {
            await output.WriteLineAsync(JsonSerializer.Serialize(new Response(1, request.Id, request.Operation, DateTimeOffset.UtcNow, [], [], []), json));
            break;
        }
        if (request.Operation is not ("inventory" or "sample" or "refresh_devices")) throw new InvalidDataException("Operación desconocida.");
        if (request.Operation == "refresh_devices") SensorProvider.Refresh();
        var results = await Task.WhenAll(slots.Values.Select(slot => slot.Get(request.Operation == "refresh_devices")));
        // Drop cached SMART entries for disks already removed from Windows inventory.
        var windowsDisks = results[2];
        if (windowsDisks.Errors.Count == 0)
        {
            var paths = windowsDisks.Devices.Select(d => d.Fields.GetValueOrDefault("path")?.Value?.ToString()?.ToLowerInvariant()).ToHashSet();
            results[4] = results[4] with { Devices = results[4].Devices.Where(d => paths.Contains(d.Fields.GetValueOrDefault("path")?.Value?.ToString()?.ToLowerInvariant())).ToList() };
            var remaining = results[4].Devices.Select(d => d.Id).ToHashSet();
            results[4] = results[4] with { Readings = results[4].Readings.Where(r => remaining.Contains(r.DeviceId)).ToList() };
        }
        var response = new Response(1, request.Id, request.Operation, DateTimeOffset.UtcNow,
            results.SelectMany(r => r.Devices).ToList(), results.SelectMany(r => r.Readings).ToList(), results.SelectMany(r => r.Errors).ToList());
        await output.WriteLineAsync(JsonSerializer.Serialize(response, json));
    }
    catch (Exception ex)
    {
        await output.WriteLineAsync(JsonSerializer.Serialize(new Response(1, request?.Id ?? "", request?.Operation ?? "", DateTimeOffset.UtcNow,
            [], [], [new("protocol", "invalid_request", ex.Message)]), json));
    }
}
// A timed out provider can still be inside native code; never close it concurrently.
if (slots.Values.All(s => !s.IsRunning)) SensorProvider.Close();

internal sealed class ProviderSlot(string name, Func<ProviderData> collect, TimeSpan interval, int timeoutMs = 1500)
{
    private Task<ProviderData>? running;
    private ProviderData last = ProviderData.Empty();
    private DateTimeOffset updated = DateTimeOffset.MinValue;
    public bool IsRunning => running is { IsCompleted: false };
    public async Task<ProviderData> Get(bool force)
    {
        if (running is null && (force || DateTimeOffset.UtcNow - updated >= interval)) running = Task.Run(collect);
        if (running is not null)
        {
            if (await Task.WhenAny(running, Task.Delay(timeoutMs)) != running)
                return Stale("timeout", "La consulta sigue en curso; se conserva el último resultado.");
            try { last = await running; }
            catch (Exception ex) { last = Stale("query_failed", ex.Message); }
            finally { running = null; updated = DateTimeOffset.UtcNow; }
        }
        return last;
    }
    private ProviderData Stale(string code, string message) => new(
        last.Devices.Select(d => d with { Fields = d.Fields.ToDictionary(f => f.Key,
            f => f.Value with { Availability = "stale", Reason = message }) }).ToList(),
        last.Readings, [new(name, code, message)]);
}
