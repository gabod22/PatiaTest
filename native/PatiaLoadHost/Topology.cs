using System.ComponentModel;
using System.Runtime.InteropServices;

namespace PatiaLoadHost;

public record LogicalCpu(ushort Group, byte Index);
public record PhysicalCore(int Id, byte Efficiency, LogicalCpu[] Threads);

internal static class Topology
{
    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool GetLogicalProcessorInformationEx(int relation, IntPtr buffer, ref uint size);
    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool SetThreadGroupAffinity(IntPtr thread, ref GroupAffinity affinity, IntPtr previous);
    [DllImport("kernel32.dll")] private static extern IntPtr GetCurrentThread();
    [StructLayout(LayoutKind.Sequential)]
    private struct GroupAffinity
    {
        public ulong Mask; public ushort Group, Reserved1, Reserved2, Reserved3;
    }
    public static PhysicalCore[] Read()
    {
        uint size = 0;
        GetLogicalProcessorInformationEx(0, IntPtr.Zero, ref size);
        if (size == 0) throw new Win32Exception(Marshal.GetLastWin32Error());
        IntPtr buffer = Marshal.AllocHGlobal(checked((int)size));
        try
        {
            if (!GetLogicalProcessorInformationEx(0, buffer, ref size)) throw new Win32Exception(Marshal.GetLastWin32Error());
            var cores = new List<PhysicalCore>();
            for (int offset = 0; offset < size;)
            {
                IntPtr entry = buffer + offset;
                int length = Marshal.ReadInt32(entry, 4);
                if (length < 32 || offset + length > size) throw new InvalidDataException("Topología incompleta.");
                byte efficiency = Marshal.ReadByte(entry, 9);
                int groups = (ushort)Marshal.ReadInt16(entry, 30);
                if (groups == 0 || 32 + groups * 16 > length) throw new InvalidDataException("Afinidades incompletas.");
                var threads = new List<LogicalCpu>();
                for (int group = 0; group < groups; group++)
                {
                    var affinity = Marshal.PtrToStructure<GroupAffinity>(entry + 32 + group * 16);
                    for (byte bit = 0; bit < 64; bit++)
                        if ((affinity.Mask & (1ul << bit)) != 0) threads.Add(new(affinity.Group, bit));
                }
                cores.Add(new(cores.Count, efficiency, threads.ToArray()));
                offset += length;
            }
            return cores.ToArray();
        }
        finally { Marshal.FreeHGlobal(buffer); }
    }
    public static void Pin(LogicalCpu cpu)
    {
        var affinity = new GroupAffinity { Group = cpu.Group, Mask = 1ul << cpu.Index };
        if (!SetThreadGroupAffinity(GetCurrentThread(), ref affinity, IntPtr.Zero)) throw new Win32Exception(Marshal.GetLastWin32Error());
    }
}
