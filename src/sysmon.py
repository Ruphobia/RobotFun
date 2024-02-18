#!/usr/bin/python3.8
import psutil
import GPUtil
import threading
import json
import time
import tornado.web

class SysMon:
    def __init__(self):
        self.lock = threading.Lock()
        self.sys_data = None
        self.running = True
        self.interval = 5  
        
        # Start the monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        self.monitor_thread.start()

    def monitor_system(self):
        """Continuously monitors system metrics including memory, temperature, and usage for CPU and GPU."""
        while self.running:
            # Query system data
            gpu_ram_status, gpu_ram_percent, gpu_ram_gb, total_gpu_ram_gb = self.get_gpu_ram_usage()
            sys_ram_status, sys_ram_percent, sys_ram_gb = self.get_system_ram()
            gpu_temp_status, gpu_count, gpu_temps, gpu_max_temp = self.get_gpu_temperatures()
            cpu_temp_status, cpu_count, cpu_temps, cpu_max_temp = self.get_cpu_temperatures()
            cpu_usage_status, cpu_usages, total_cpu_usage = self.get_cpu_usage()
            gpu_usage_status, gpu_loads, max_gpu_load = self.get_gpu_usage()

            # Check status of all queries
            if any(status == -1 for status in [gpu_ram_status, sys_ram_status, gpu_temp_status, cpu_temp_status, cpu_usage_status, gpu_usage_status]):
                print("Error: One or more system monitors failed.")
            else:
                # Construct JSON object with all collected data
                data = {
                    "gpu_ram_percent": gpu_ram_percent,
                    "gpu_ram_gb": gpu_ram_gb,
                    "total_gpu_ram_gb": total_gpu_ram_gb,
                    "sys_ram_percent": sys_ram_percent,
                    "sys_ram_gb": sys_ram_gb,
                    "gpu_temps": gpu_temps,
                    "gpu_max_temp": gpu_max_temp,
                    "cpu_temps": cpu_temps,
                    "cpu_max_temp": cpu_max_temp,
                    "cpu_usages": cpu_usages,
                    "total_cpu_usage": total_cpu_usage,
                    "gpu_loads": gpu_loads,
                    "max_gpu_load": max_gpu_load
                }

                # Acquire lock and update sys_data
                with self.lock:
                    self.sys_data = data

            time.sleep(self.interval)

    def get_sys_data(self):
        """
        Returns the system monitoring data.

        Returns:
        dict: A dictionary containing the system monitoring data.
        """
        with self.lock:
            return self.sys_data

    def start_monitoring(self):
        """Starts monitoring the system."""
        self.running = True

    def stop_monitoring(self):
        """Stops monitoring the system."""
        self.running = False
        
    def get_cpu_temperatures(self) -> tuple:
        """
        Retrieves the temperature of each CPU core in Fahrenheit using psutil library.

        Returns:
        tuple: A tuple containing the status code, count of CPU cores, a list of CPU temperatures in Fahrenheit,
            and the maximum temperature among all CPU cores.
            Status code: -1 for failure, 0 for success.
            Count of CPU cores: Number of CPU cores detected.
            List of CPU temperatures: Temperatures of each CPU core in Fahrenheit.
            Max temperature: Maximum temperature among all CPU cores.
        """
        try:
            cpu_temps = []
            temps = psutil.sensors_temperatures()
            max_temp = float('-inf')
            if 'coretemp' in temps:
                for temp in temps['coretemp']:
                    temp_fahrenheit = temp.current * 9/5 + 32
                    cpu_temps.append(temp_fahrenheit)
                    max_temp = max(max_temp, temp_fahrenheit)
                return 0, len(cpu_temps), cpu_temps, max_temp
            else:
                print("Couldn't fetch CPU temperatures. Make sure the hardware and OS support this feature.")
                return -1, 0, [], float('-inf')
        except Exception as e:
            print(f"Error occurred: {e}")
            return -1, 0, [], float('-inf')
        
    def get_gpu_temperatures(self) -> tuple:
        """
        Retrieves the temperature of each GPU in Fahrenheit using GPUtil library.

        Returns:
        tuple: A tuple containing the status code, count of GPU cards, a list of GPU temperatures in Fahrenheit,
            and the maximum temperature among all GPUs.
            Status code: -1 for failure, 0 for success.
            Count of GPU cards: Number of GPU cards detected.
            List of GPU temperatures: Temperatures of each GPU in Fahrenheit.
            Max temperature: Maximum temperature among all GPUs.
        """
        try:
            gpu_temps = []
            gpus = GPUtil.getGPUs()
            max_temp = float('-inf')
            for gpu in gpus:
                temp_fahrenheit = gpu.temperature * 9/5 + 32
                gpu_temps.append(temp_fahrenheit)
                max_temp = max(max_temp, temp_fahrenheit)
            return 0, len(gpus), gpu_temps, max_temp
        except Exception as e:
            print(f"Error occurred: {e}")
            return -1, 0, [], float('-inf')
        
    def get_cpu_usage(self) -> tuple:
        """
        Retrieves CPU usage information.

        Returns:
        tuple: A tuple containing the status code, list of CPU usages for each core, and the total CPU usage.
            Status code: -1 for failure, 0 for success.
            List of CPU usages: CPU usage percentage for each CPU core.
            Total CPU usage: Total CPU usage percentage by combining all CPU cores.
        """
        try:
            cpu_usage = psutil.cpu_percent(percpu=True)
            total_cpu_usage = sum(cpu_usage) / len(cpu_usage)
            return 0, cpu_usage, total_cpu_usage
        except Exception as e:
            print(f"Error occurred: {e}")
            return -1, [], 0
        
    import GPUtil

    def get_gpu_usage(self) -> tuple:
        """
        Retrieves GPU usage information.

        Returns:
        tuple: A tuple containing the status code, list of GPU loads for each GPU, and the maximum GPU load.
            Status code: -1 for failure, 0 for success.
            List of GPU loads: GPU load percentage for each available GPU.
            Maximum GPU load: Highest GPU load percentage among all GPUs.
        """
        try:
            gpus = GPUtil.getGPUs()
            gpu_loads = [gpu.load * 100 for gpu in gpus]  # Convert load fraction to percentage
            max_gpu_load = max(gpu_loads) if gpu_loads else 0
            return 0, gpu_loads, max_gpu_load
        except Exception as e:
            print(f"Error occurred: {e}")
            return -1, [], 0

        

    def get_system_ram(self) -> tuple:
        """
        Retrieves system RAM information.

        Returns:
        tuple: A tuple containing the status code, RAM percentage in use, and RAM in use in gigabytes.
            Status code: -1 for failure, 0 for success.
            RAM percentage in use: Percentage of RAM in use.
            RAM in use (GB): Amount of RAM in use in gigabytes (formatted to two decimal places).
        """
        try:
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_gb_in_use = round(ram.used / (1024 ** 3), 2)  # Convert bytes to gigabytes and round to two decimal places
            return 0, ram_percent, ram_gb_in_use
        except Exception as e:
            print(f"Error occurred: {e}")
            return -1, 0, 0
        
    def get_gpu_ram_usage(self) -> tuple:
        """
        Retrieves GPU RAM usage information.

        Returns:
        tuple: A tuple containing the status code, list of GPU RAM usage percentages,
            list of GPU RAM usage in gigabytes, and total GPU RAM usage in gigabytes.
            Status code: -1 for failure, 0 for success.
            List of GPU RAM usage percentages: Percentage of GPU RAM usage for each GPU.
            List of GPU RAM usage (GB): Amount of GPU RAM usage for each GPU in gigabytes (formatted to two decimal places).
            Total GPU RAM usage (GB): Total amount of GPU RAM usage across all GPUs in gigabytes (formatted to two decimal places).
        """
        try:
            gpu_percent_used = []
            gpu_gb_used = []
            total_gb_used = 0

            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                gpu_percent_used.append(gpu.memoryUtil * 100)
                gpu_gb_used.append(round(gpu.memoryUsed / 1024, 2))  # Convert to gigabytes and round to two decimal places
                total_gb_used += gpu.memoryUsed / 1024

            total_gb_used = round(total_gb_used, 2)

            return 0, gpu_percent_used, gpu_gb_used, total_gb_used
        except Exception as e:
            print(f"Error occurred: {e}")
            return -1, [], [], 0
    
class SysMonHandler(tornado.web.RequestHandler):
    def initialize(self, sysmon_instance):
        self.sysmon = sysmon_instance

    def get(self):
        sys_data = self.sysmon.get_sys_data()
        self.write(json.dumps(sys_data))

    
