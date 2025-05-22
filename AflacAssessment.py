#!/usr/bin/env python3

import os
import psutil
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import shutil
import time

# CONFIGURATION
ALERT_EMAIL = "admin@example.com"
CRITICAL_DISK_THRESHOLD = 90  # in percent
CPU_THRESHOLD = 85  # in percent
MEMORY_THRESHOLD = 85  # in percent
LOG_FILE_PATH = "/var/log/syslog"
KEYWORDS = ["ERROR", "CRITICAL", "FAILURE"]
BACKUP_SOURCE_DIRS = ["/etc", "/home"]
BACKUP_DESTINATION = "/mnt/backup"
USER_ACTIVITY_LOG = "/var/log/user_activity.log"
SERVICES_TO_MONITOR = ["apache2", "mysql"]  # Example services
MONITOR_DURATION = 5 * 60 * 60  # 5 hours in seconds

# Email simulation function
def send_email(subject, message):
    print(f"Simulated Email Sent to {ALERT_EMAIL}: {subject}\n{message}\n")

# Task 1: Disk Usage Monitoring & Notification
def monitor_disk_usage():
    for partition in psutil.disk_partitions():
        if os.name == 'nt':
            if 'cdrom' in partition.opts or partition.fstype == '':
                continue
        usage = psutil.disk_usage(partition.mountpoint)
        if usage.percent >= CRITICAL_DISK_THRESHOLD:
            send_email("Disk Usage Alert", f"Disk usage on {partition.device} is at {usage.percent}%.")

# Task 2: Service Monitoring & Restart
def monitor_services():
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            run_time = time.time() - proc.info['create_time']
            if run_time > MONITOR_DURATION and proc.info['name'] in SERVICES_TO_MONITOR:
                os.system(f"sudo systemctl restart {proc.info['name']}")
                send_email("Service Restarted", f"Restarted service: {proc.info['name']} after running for more than 5 hours.")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

# Task 3: Log File Monitoring
def monitor_log_file():
    with open(LOG_FILE_PATH, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            if any(keyword in line for keyword in KEYWORDS):
                send_email("Log Alert", f"Alert keyword detected: {line.strip()}")

# Task 4: Automated Backup Script
def perform_backup():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_name = f"backup_{timestamp}.tar.gz"
    backup_path = os.path.join(BACKUP_DESTINATION, backup_name)
    os.makedirs(BACKUP_DESTINATION, exist_ok=True)
    backup_command = f"tar -czf {backup_path} {' '.join(BACKUP_SOURCE_DIRS)}"
    os.system(backup_command)
    send_email("Backup Completed", f"Backup saved to {backup_path}")

# Task 5: User Activity Tracker
def track_user_activity():
    os.system(f"last -w > {USER_ACTIVITY_LOG}")

# Task 6: CPU/Memory Usage Alert
def monitor_cpu_memory():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    if cpu > CPU_THRESHOLD:
        send_email("CPU Alert", f"CPU usage is high: {cpu}%")
    if memory > MEMORY_THRESHOLD:
        send_email("Memory Alert", f"Memory usage is high: {memory}%")

# Example scheduler for backup (can be replaced with cron)
if __name__ == '__main__':
    monitor_disk_usage()
    monitor_services()
    track_user_activity()
    monitor_cpu_memory()
    # Uncomment the next line to run backup and log monitor
    # perform_backup()
    # monitor_log_file()  # Run this in a separate thread or process
