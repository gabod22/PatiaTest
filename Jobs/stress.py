from PySide6.QtCore import Signal, QObject
import psutil
from time import sleep
from datetime import datetime
from multiprocessing import Process, active_children, Pipe
TOTAL_CPU = psutil.cpu_count(logical=True)
PERCENT = 100


class StressCPU(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hora_inicio = datetime.now()
        print(self.hora_inicio)
        self._stopped = False
        self._stopStressTest = False
        # self.batteries = batteries
        self.WAIT_TIME = 60  # seconds
        # self.HOURS_CONVERSION_CONSTANT= 3600/self.WAIT_TIME
        self.proc_num = TOTAL_CPU

        self.procs = []
        self.conns = []

    def loop(self, conn, affinity, check):
        '''
        Function to stress cores to run at 100%

        Arguments:
            conn    : child connection which is an object of Pipe()
            affinity: list of cores to assign affinity for the process
            check   : conditional flag to enable real time calibration
        '''
        proc = psutil.Process()
        proc_info = proc.pid
        # Create a message string of PID and core number
        msg = "Process ID: "+str(proc_info)+" CPU: "+str(affinity[0])
        conn.send(msg)  # Send message to parent
        conn.close()
        proc.cpu_affinity(affinity)  # Assigns a core to process
        while True:
            '''
            Conditional check for calibration
            '''
            if(check and psutil.cpu_percent() > PERCENT):
                sleep(0.05)  # Change the time for finetuning
            1*1

    def last_core_loop(self, conn, affinity, percent):
        '''
        Function to stress the last core at fractional percentage.
        e.g. core 5 at 45% Usage

        Arguments:
            conn    : child connection which is an object of Pipe()
            affinity: list of cores to assign affinity for the process
            percent   : fractional percentage to run the core at
        '''
        proc = psutil.Process()
        proc_info = proc.pid
        # Create a message string of PID and core number
        msg = "Process ID: "+str(proc_info)+" CPU: "+str(affinity[0])
        conn.send(msg)  # Send message to parent
        conn.close()
        proc.cpu_affinity(affinity)  # Assigns a core to process
        while True:
            '''
            Conditional check for core calibration
            '''
            if(psutil.cpu_percent(percpu=True)[affinity[0]] > percent):
                sleep(0.1)  # Change the time for finetuning
            1*1

    def start_stress_test(self):
        '''
        CPU Stress logic:
        '''

        print("Stressing %f cores:" % (self.proc_num))
        actual_cores = int(self.proc_num)
        last_core_usage = round((self.proc_num-actual_cores), 2)*100
        self.proc_num = actual_cores

        # Run the required cores at 100% except one
        for i in range(self.proc_num-1):
            parent_conn, child_conn = Pipe()
            p = Process(target=self.loop, args=(child_conn, [i], False))
            p.start()
            self.procs.append(p)
            self.conns.append(parent_conn)

        # Run the last core out of the required cores to balance total output by actively calibrating realtime usage
        parent_conn, child_conn = Pipe()
        p = Process(target=self.loop, args=(
            child_conn, [self.proc_num-1], True))
        p.start()
        self.procs.append(p)
        self.conns.append(parent_conn)

        # If CPU usage is not 100%, run the fractional part of the last core
        if(self.proc_num != TOTAL_CPU):
            last_core = self.proc_num
            parent_conn, child_conn = Pipe()
            p = Process(target=self.last_core_loop, args=(
                child_conn, [last_core], last_core_usage))
            p.start()
            self.procs.append(p)
            self.conns.append(parent_conn)

        # Print PID and core messages sent by the children
        for conn in self.conns:
            try:
                print(conn.recv())
            except EOFError:
                continue

        def stop_stress_test(self):
            for p in self.procs:
                p.terminate()