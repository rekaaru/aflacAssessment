# aflacAssessment

Readme
System Administration Scripts
This repository contains a collection of Python scripts to automate common system administration tasks. These scripts are useful for system monitoring, maintenance, and backup operations.

Features
1. Disk Usage Monitoring & Notification
Monitors disk usage across mounted partitions. Sends a simulated email alert if usage exceeds a specified threshold (default: 90%).

2. Service Monitoring & Restart
Identifies specific services/processes that have been running for more than 5 hours. Automatically restarts them and logs the action.

3. Log File Monitoring
Watches a designated log file (e.g., /var/log/syslog) in real-time for critical keywords like ERROR, CRITICAL, or FAILURE. Simulated email notifications are sent when these are detected.

4. Automated Backup Script
Creates compressed backups of specified directories (e.g., /etc, /home). Each backup is timestamped and stored in a designated destination directory (e.g., /mnt/backup). Can be scheduled via cron.

5. User Activity Tracker
Tracks user login and logout activities using the last command. Outputs are saved in a daily report (/var/log/user_activity.log).

6. CPU/Memory Usage Alert
Monitors system CPU and memory usage. Sends alerts if usage exceeds defined thresholds (default: 85%).

Requirements
Python 3.x

psutil library (pip install psutil)

Usage
Run the main script as root or with sufficient privileges:

sudo python3 system_admin_scripts.py
Note: The log file monitor (monitor_log_file()) runs indefinitely. It is recommended to run it in a separate process or thread.

Configuration
Modify the following variables in the script as needed:

ALERT_EMAIL: Email address for simulated alerts

CRITICAL_DISK_THRESHOLD: Disk usage alert level

CPU_THRESHOLD & MEMORY_THRESHOLD: CPU/Memory alert levels

LOG_FILE_PATH: Path to the system log file

BACKUP_SOURCE_DIRS & BACKUP_DESTINATION: Backup source and destination directories

SERVICES_TO_MONITOR: List of services to monitor for long runtime

Scheduling
Use cron to automate tasks such as backups or user activity tracking. Example cron job for daily backups:

0 2 * * * /usr/bin/python3 /path/to/system_admin_scripts.py >> /var/log/backup.log 2>&1

Feel free to modify and extend these scripts as per your environment's requirements.


