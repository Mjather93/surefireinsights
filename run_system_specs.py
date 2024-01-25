import argparse
import platform
import sqlite3
import cpuinfo
import psutil
import json
import re
import socket
import uuid
from datetime import datetime


# Import args
argParser = argparse.ArgumentParser()
argParser.add_argument("-rp", "--report_pk", help="Path to the config.yaml file")
args = argParser.parse_args()
report_pk = args.report_pk

def get_size(memorysize, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if memorysize < factor:
            return f"{memorysize:.2f}{unit}{suffix}"
        memorysize /= factor


def system_information():
    uname = platform.uname()
    system_name = uname.node
    system_type = uname.system
    system_release_version_major = uname.release
    system_release_version_minor = uname.version
    machine_type = uname.machine
    processor_type = uname.processor
    processor_spec = cpuinfo.get_cpu_info()['brand_raw']
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    last_boot_time = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
    physical_core_count = psutil.cpu_count(logical=False)
    total_core_count = psutil.cpu_count(logical=True)
    cpufreq = psutil.cpu_freq()
    max_core_frequency = f"{cpufreq.max:.2f}Mhz"
    svmem = psutil.virtual_memory()
    total_memory = get_size(svmem.total)
    partitions_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_info = {
            "Device": partition.device,
            "Mountpoint": partition.mountpoint,
            "File system type": partition.fstype
        }

        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # Handle PermissionError as needed
            continue
        partition_info["Total Size"] = get_size(partition_usage.total)
        partition_info["Used"] = get_size(partition_usage.used)
        partition_info["Free"] = get_size(partition_usage.free)
        partition_info["Percentage"] = partition_usage.percent
        partitions_info[partition.device] = partition_info
    disk_information = json.dumps(partitions_info, indent=4)

    # Insert the system specs metrics into the system_metrics table of the sqlite db
    connection = sqlite3.connect('surefireinsights.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO system_specs
        (system_name, system_type, system_release_version_major, system_release_version_minor,
        machine_type, processor_type, processor_spec, ip_address, mac_address, last_boot_time,
        physical_core_count, total_core_count, max_core_frequency, total_memory, disk_information, report_fk)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (system_name, system_type, system_release_version_major, system_release_version_minor,
          machine_type, processor_type, processor_spec, ip_address, mac_address, last_boot_time,
          physical_core_count, total_core_count, max_core_frequency, total_memory, disk_information, report_pk))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    system_information()
