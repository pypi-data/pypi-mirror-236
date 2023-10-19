import psutil
import time
import gc
import threading
import json
# from cpumonitor import CPUMonitor

class CPUMonitor:
    def __init__(self, interval=1.0):
        self.interval = interval
        self.peak_cpu = 0
        self._stop_event = threading.Event()
        # print("..cpumonitor initialized with interval of: " + str(self.interval) + " seconds")

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        # print("..cpumonitor(ing) started")

    def stop(self):
        self._stop_event.set()
        self.thread.join()
        # print("..cpumonitor(ing) stopped")

    def run(self):
        while not self._stop_event.is_set():
            cpu = psutil.cpu_percent()
            if cpu > self.peak_cpu:
                self.peak_cpu = cpu
                # print(f"Peak CPU usage changed to: {self.peak_cpu}%")
            time.sleep(self.interval)

class Measure:
    def __init__(self, pid=0, useCpuMonitor=False, cpuMonitorInterval=1.0):
        if pid == 0:
            pid = psutil.Process().pid
            
        self.pid = pid
        self.useCpuMonitor = useCpuMonitor
        self.cpuMonitorInterval = cpuMonitorInterval

        self.start_memory = self.get_current_mem_wset()
        self.start_time = time.time()
        # print(f"..Object creation time mem usage: {int(self.start_memory):,} KBs")

    def start(self):
        self.start_time = time.time()
        self.start_memory = self.get_current_mem_wset()
        # print(f"..Starting out mem usage: {int(self.start_memory):,} KBs")
        if self.useCpuMonitor:
            self.monitor = CPUMonitor(self.cpuMonitorInterval)
            self.monitor.start()
        else:
            print("..(not using cpumonitor)")

    def end(self):
        end_time = time.time()
        if self.useCpuMonitor:
            self.monitor.stop()
            print(" ----------------------------------------- ")
            print(f" > Peak CPU usage: {self.monitor.peak_cpu}%'")

        end_memory = self.get_current_mem_wset()
        end_peak_memory = self.get_current_mem_peak_wset()

        timely_mem_usage = end_peak_memory - self.start_memory
        time_taken_sec = (end_time - self.start_time)

        print(f" > Memory surge/usage: {int(timely_mem_usage):,} KBs ({int(self.start_memory):,} KBs -> {int(end_peak_memory):,} KBs)")
        print(f" > Time taken: {time_taken_sec:,} sec")
        print(" ----------------------------------------- ")
        
        # Force garbage collection
        gc.collect()

        # Create a dictionary with the extracted information
        cpu_usage = self.monitor.peak_cpu if self.useCpuMonitor else 0
        memory_usage = int(timely_mem_usage)
        time_taken = time_taken_sec

        data = {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "time_taken": time_taken,
        }

        # Convert the dictionary to a JSON object
        json_data = json.dumps(data)

        return json_data
    
    def get_current_mem_wset(self):
        return psutil.Process(self.pid).memory_full_info().wset / 1024

    def get_current_mem_peak_wset(self):
        return psutil.Process(self.pid).memory_full_info().peak_wset / 1024
