import os
import sys
import signal
import psutil
from datetime import datetime
import json
import sched
import time
import logging

class Daemonized:
    def __init__(self, pidfile, run, port, workers):
        self.pidfile = pidfile
        self.run = run
        self.port = port
        self.workers = workers
        self.monitoring_data = []
        self.monitoring_data_file = os.path.expanduser('~/.netix/daemon/monitoring.json')

    def save_pid(self, pid):
        pid_dir = os.path.expanduser('~/.netix/daemon')
        os.makedirs(pid_dir, exist_ok=True)
        pid_file_path = os.path.join(pid_dir, self.pidfile)

        with open(pid_file_path, 'a') as pidfile:
            pidfile.write(str(pid) + '\n')

    def get_pids(self):
        pid_dir = os.path.expanduser('~/.netix/daemon')
        pid_file_path = os.path.join(pid_dir, self.pidfile)
        pids = []
        if os.path.exists(pid_file_path):
            with open(pid_file_path, 'r') as pidfile:
                pids = [int(line.strip()) for line in pidfile.readlines()]
        return pids

    def daemonize(self):
        if os.name == 'nt':
            print("Daemon mode is not supported on Windows.")
            sys.exit(1)

        if os.fork() != 0:
            sys.exit(0)

        os.setsid()
        os.umask(0)

        if os.fork() != 0:
            sys.exit(0)

        sys.stdout.flush()
        sys.stderr.flush()

        pid_dir = os.path.expanduser('~/.netix/daemon')
        os.makedirs(pid_dir, exist_ok=True)
        pid_file_path = os.path.join(pid_dir, self.pidfile)

        with open(pid_file_path, 'w') as pidfile:
            pidfile.write(str(os.getpid()) + '\n')

    def start(self):
        self.daemonize()
        self.update_monitoring_data()
        pid = os.fork()
        if pid == 0:
            self.save_pid(os.getpid())  # Save child PID
            self.redirect_output()
            self.run()
        else:
            self.save_pid(pid)  # Save the first forked child PID

    def stop(self, specific_port=None, specific_name=None):
        pids = self.get_pids()
        if not pids:
            print("No server processes are running.")
            return

        for pid in pids:
            try:
                process_name = self.get_process_name(pid)
                port = self.get_process_port(pid)
                if (specific_port and specific_port == port) or (specific_name and specific_name == process_name):
                    os.kill(pid, signal.SIGTERM)
                    print(f"Stopped server process (PID {pid}) for port {port}")
                elif not specific_port and not specific_name:
                    os.kill(pid, signal.SIGTERM)
                    print(f"Stopped server process (PID {pid}) for port {port}")
            except ProcessLookupError:
                pass

    def restart(self, specific_port=None, specific_name=None):
        pids = self.get_pids()
        if not pids:
            print("No server processes are running.")
            return

        for pid in pids:
            try:
                process_name = self.get_process_name(pid)
                port = self.get_process_port(pid)
                if (specific_port and specific_port == port) or (specific_name and specific_name == process_name):
                    os.kill(pid, signal.SIGHUP)
                    print(f"Restarted server process (PID {pid}) for port {port}")
                elif not specific_port and not specific_name:
                    os.kill(pid, signal.SIGHUP)
                    print(f"Restarted server process (PID {pid}) for port {port}")
            except ProcessLookupError:
                pass

    def graceful_shutdown(self, specific_port=None, specific_name=None):
        pids = self.get_pids()
        if not pids:
            print("No server processes are running.")
            return

        for pid in pids:
            try:
                process_name = self.get_process_name(pid)
                port = self.get_process_port(pid)
                if (specific_port and specific_port == port) or (specific_name and specific_name == process_name):
                    os.kill(pid, signal.SIGINT)
                    print(f"Gracefully shut down server process (PID {pid}) for port {port}")
                elif not specific_port and not specific_name:
                    os.kill(pid, signal.SIGINT)
                    print(f"Gracefully shut down server process (PID {pid}) for port {port}")
            except ProcessLookupError:
                pass

    def get_process_name(self, pid):
        try:
            process = psutil.Process(pid)
            return process.name()
        except psutil.NoSuchProcess:
            return "Unknown"

    def get_process_port(self, pid):
        try:
            process = psutil.Process(pid)
            cmdline = process.cmdline()
            for i, part in enumerate(cmdline):
                if part == "--port" and i + 1 < len(cmdline):
                    return int(cmdline[i + 1])
            return "Unknown"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return "Unknown"

    def get_process_memory(self, pid):
        try:
            process = psutil.Process(pid)
            memory_info = process.memory_info()
            return memory_info.rss
        except psutil.NoSuchProcess:
            return 0

    def get_process_cpu_usage(self, pid):
        try:
            process = psutil.Process(pid)
            return process.cpu_percent(interval=0.1)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0

    def get_process_start_time(self, pid):
        try:
            process = psutil.Process(pid)
            start_time = process.create_time()
            return datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return "Unknown"

    def get_process_thread_count(self, pid):
        try:
            process = psutil.Process(pid)
            return process.num_threads()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0

    def get_process_open_file_count(self, pid):
        try:
            process = psutil.Process(pid)
            return process.num_fds()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0
        
    def check_monitoring_status(self):
        # Load existing monitoring data
        existing_data = []
        try:
            with open(self.monitoring_data_file, "r") as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            pass  # If the file doesn't exist, there is no existing data to update

        updated_data = []

        for data in existing_data:
            pid = data["PID"]
            status = "online" if self.is_process_running(pid) else "offline"
            if status == "online":
                # Only update data for running processes
                process = psutil.Process(pid)
                io_counter = process.io_counters()
                connections = process.connections()
                data["Status"] = status
                data['Memory Usage'] = self.get_process_memory(pid)
                data['Process Status'] = process.status()
                data['CPU Usage'] = self.get_process_cpu_usage(pid)
                data['Thread Count'] = self.get_process_thread_count(pid)
                data['Open File Count'] = self.get_process_open_file_count(pid)
                data['I/O Counters']['Read Count'] = io_counter.read_count
                data['I/O Counters']['Write Count'] = io_counter.write_count
                data['I/O Counters']['Read Bytes'] = io_counter.read_bytes
                data['I/O Counters']['Write Bytes'] = io_counter.write_bytes
                data['Network Connections'] = [conn.laddr for conn in connections]
                updated_data.append(data)
            else:
                # The process is no longer running, so remove it from the monitoring data
                raise Exception(f"Process with PID {pid} is no longer running.")
        
        if not updated_data:
            # No running processes, stop the scheduler
            raise Exception("All monitored processes have stopped. Stopping the scheduler.")
            
        # Update the monitoring data with updated statuses
        with open(self.monitoring_data_file, "w") as json_file:
            json.dump(updated_data, json_file, indent=4)
        
    def update_monitoring_data(self):
        try:
            pids = self.get_pids()

            monitoring_data = []

            for pid in pids:
                process = psutil.Process(pid)
                process_status = process.status()
                process_name = process.name()
                port = self.port
                workers = self.workers
                memory_info = process.memory_info()
                cpu_percent = self.get_process_cpu_usage(pid)
                start_time = self.get_process_start_time(pid)
                thread_count = self.get_process_thread_count(pid)
                open_file_count = self.get_process_open_file_count(pid)
                status = "online" if self.is_process_running(pid) else "offline"
                username = psutil.Process(pid).username()
                ppid = process.ppid()
                io_counters = process.io_counters()
                cwd = process.cwd()
                connections = process.connections()
                cmd = process.cmdline()

                new_data = {
                    "PID": pid,
                    "Process Name": process_name,
                    "Port": port,
                    'Workers': workers,
                    "Memory Usage": memory_info.rss,
                    "CPU Usage": round(cpu_percent, 2),
                    "Start Time": start_time,
                    "Thread Count": thread_count,
                    "Open File Count": open_file_count,
                    "Status": status,
                    "Username": username,
                    "PPID": ppid,
                    "Network Connections": [conn.laddr for conn in connections],
                    "I/O Counters": {
                        "Read Count": io_counters.read_count,
                        "Write Count": io_counters.write_count,
                        "Read Bytes": io_counters.read_bytes,
                        "Write Bytes": io_counters.write_bytes
                    },
                    "Working Directory": cwd,
                    "Command Line Argument": cmd,
                    "Process Status": process_status
                }

                monitoring_data.append(new_data)
            
            # If the monitoring JSON file doesn't exist, create it and insert the data
            if not os.path.exists(self.monitoring_data_file):
                with open(self.monitoring_data_file, "w") as json_file:
                    json.dump(monitoring_data, json_file, indent=4)
            else:
                # Load existing monitoring data
                existing_data = []
                try:
                    with open(self.monitoring_data_file, "r") as json_file:
                        existing_data = json.load(json_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    existing_data = []

                # Append new data to the existing data
                existing_data.extend(monitoring_data)

                # Update the monitoring data in the JSON file
                with open(self.monitoring_data_file, "w") as json_file:
                    json.dump(existing_data, json_file, indent=4)
        
        except Exception as e:
            logging.error(f"Failed to update monitoring data: {str(e)}")

    def is_process_running(self, pid):
        return pid in psutil.pids()

    def redirect_output(self):
        devnull = os.open(os.devnull, os.O_RDWR)
        os.dup2(devnull, sys.stdin.fileno())
        os.dup2(devnull, sys.stdout.fileno())
        os.dup2(devnull, sys.stderr.fileno())