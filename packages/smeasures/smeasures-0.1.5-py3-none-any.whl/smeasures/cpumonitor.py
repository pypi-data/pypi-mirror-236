import psutil
import time
import threading

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
