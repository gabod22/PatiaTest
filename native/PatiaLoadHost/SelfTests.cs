namespace PatiaLoadHost;

internal static class SelfTests
{
    public static void Run()
    {
        int checks = 0;
        void Check(bool condition, string message) { if (!condition) throw new Exception(message); checks++; }
        Check(Feedback.Next(.5, 20, 60) < .5, "Reducir ante actividad externa");
        Check(Feedback.Next(.5, 60, 20) > .5, "Aumentar carga");
        Check(Feedback.ExternalCpu(80, 30) == 50, "Actividad externa separada del auxiliar");
        Check(Feedback.ExternalCpu(10, 12) == 0 && Feedback.ExternalCpu(null, 10) is null, "Ruido y ausencia de medición");
        Check(Feedback.Next(.5, 50, 50, 100, 80) < Feedback.Next(.5, 50, 50), "Anticipar aumento externo sin esperar la media");
        Check(Feedback.Next(1, 100, 0) == 1 && Feedback.Next(.5, 0, 80) == 0, "Límites y cero");
        foreach (double target in new[] { 0d, 20, 30, 50, 100 })
        {
            double duty = 0; var average = new Queue<double>();
            for (int second = 0; second < 240; second++)
            {
                double external = second < 60 ? 0 : second < 120 ? 15 : second < 180 ? 0 : Math.Min(100, target + 20);
                double actual = Math.Min(100, external + duty * 100);
                average.Enqueue(actual); while (average.Count > 3) average.Dequeue();
                duty = Feedback.Next(duty, target, average.Average(), 100, actual);
                if (second is 59 or 119 or 179)
                    Check(target == 0 ? duty == 0 : Math.Abs(actual - target) <= 5, "Estabilidad tras cambio externo");
                if (second == 239 && target < 100) Check(duty < .001, "No añadir carga sobre el objetivo");
            }
        }
        PhysicalCore[] hybrid = [new(0, 1, [new(0, 0), new(0, 1)]), new(1, 1, [new(0, 2), new(0, 3)]),
                                 new(2, 0, [new(1, 0)]), new(3, 0, [new(1, 1)])];
        Check(CpuLoad.RequiredCores(hybrid, 20) == 1, "Núcleo con SMT");
        Check(CpuLoad.RequiredCores(hybrid, 70) == 3, "Ampliación híbrida y grupos");
        Check(CpuLoad.RequiredCores(hybrid, 100) == 4, "Todos los núcleos");
        var counters = new (string, double)[] {
            ("pid_1_luid_0x00000001_0x00000002_phys_0_eng_0_engtype_3D", 20),
            ("pid_2_luid_0x00000001_0x00000002_phys_0_eng_0_engtype_3D", 30),
            ("pid_1_luid_0x00000001_0x00000002_phys_0_eng_1_engtype_Copy", 10),
            ("pid_1_luid_0x00000000_0x00000002_phys_0_eng_0_engtype_3D", 100) };
        Check(Counters.Aggregate(counters, "100000002") == 50, "LUID y máximo por motor, sumando procesos");
        Check(Counters.Aggregate(counters, "123") is null, "Adaptador desaparecido/sin contadores");
        Console.WriteLine($"PASS: {checks} comprobaciones de regulación, topología y contadores GPU");
    }
}
