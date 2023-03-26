# px-nodes-output.csv
import csv
import pandas as pd

data = pd.read_csv(r'px-nodes-output.csv')

# Prints whole CSV
# print(data)

df = pd.DataFrame(data, columns=['node', 'actual_disk_read_throughput', 'actual_disk_write_throughput', 'total_disk_read_throughput', 'total_disk_write_throughput', 'rss', 'vsize', 'cpu_usage', 'time_'])
#print(df['total_disk_read_throughput'])

actual_disk_read_throughput_average = 0
actual_disk_write_throughput_average = 0
total_disk_read_throughput_average = 0
total_disk_write_throughput_average = 0
rss_average = 0
vsize_average = 0
cpu_usage_average = 0
total_values = 0




# 1) Format text
# Calculating Average for Actual Disk Read Throughput

for val in df['actual_disk_read_throughput']:
    if not isinstance(val, float):
        length = len(val)
        str = val[length - 5:]
        if str == "B/sec":
            total_values += 1
            actual_disk_read_throughput_average += float(val.replace(" B/sec", ""))
        elif val == "tx_bytes_per_ns":
            actual_disk_read_throughput_average = round(actual_disk_read_throughput_average / total_values, 4)
            total_values = 0
            break

#Calculating Average for Actual Disk Write Throughput

for val in df['actual_disk_write_throughput']:
    if not isinstance(val, float):
        length = len(val)
        str = val[length - 7:]
        if str == "KiB/sec":
            total_values += 1
            actual_disk_write_throughput_average += float(val.replace("KiB/sec", ""))
        elif val == "rx_bytes_per_ns":
            actual_disk_write_throughput_average = round(actual_disk_write_throughput_average / total_values, 4)
            total_values = 0
            break

#Calculating Average for Total Disk Read Throughput

for val in df['total_disk_read_throughput']:
    if not isinstance(val, float):
        length = len(val)
        str = val[length - 7:]
        if str == "KiB/sec":
            total_values += 1
            total_disk_read_throughput_average += float(val.replace(" KiB/sec", ""))
        if str == "MiB/sec":
            total_values += 1
            total_disk_read_throughput_average += (float(val.replace(" MiB/sec", "")) * 1024)
        elif val == "tx_bytes_per_ns":
            total_disk_read_throughput_average /= total_values
            total_disk_read_throughput_average = round(total_disk_read_throughput_average/1024, 4) 
            total_values = 0
            break

#Calculating Average for Total Disk Write Throughput

for val in df['total_disk_write_throughput']:
    if not isinstance(val, float):
        length = len(val)
        str = val[length - 7:]
        if str == "KiB/sec":
            total_values += 1
            total_disk_write_throughput_average += float(val.replace(" KiB/sec", ""))
        elif val == "rx_drop_per_ns":
            total_disk_write_throughput_average= round(total_disk_write_throughput_average / total_values, 4)
            total_values = 0
            break

#Calculating Average for RSS

for val in df['rss']:
    if not isinstance(val, float):
        length = len(val)
        str = val[length - 3:]
        if str == "GiB":
            total_values += 1
            rss_average += float(val.replace(" GiB", ""))
        elif val == "tx_drops_per_ns":
            rss_average = round(rss_average / total_values, 4)
            total_values = 0
            break

#Calculating Average for V-Size

for val in df['vsize']:
    if not isinstance(val, float):
        length = len(val)
        str = val[length - 3:]
        if str == "GiB":
            total_values += 1
            vsize_average += float(val.replace(" GiB", ""))
        elif val == "rx_errors_per_ns":
            vsize_average = round(vsize_average / total_values, 4)
            total_values = 0
            break

#Calculating Average for CPU Usage

for val in df['cpu_usage']:
    if not isinstance(val, float):
        length = len(val)
        str = val[length - 1:]
        if str == "%":
            total_values += 1
            cpu_usage_average += float(val.replace("%", ""))
        elif val == "tx_errors_per_ns":
            cpu_usage_average = round(cpu_usage_average / total_values, 4)
            total_values = 0
            break

# 2) Store averages into variables


print(f"Actual Read Throughput Average: {actual_disk_read_throughput_average} B/sec")
print(f"Actual Write Throughput Average: {actual_disk_write_throughput_average} KiB/sec")
print(f"Total Read Throughtput Average: {total_disk_read_throughput_average} KiB/sec")
print(f"Total Write Throughtput Average: {total_disk_write_throughput_average} KiB/sec")
print(f"RSS Average: {rss_average} GiB")
print(f"Vsize Average: {vsize_average} GiB")
print(f"CPU Usage Average: {cpu_usage_average}%")

# ... compare with previous values