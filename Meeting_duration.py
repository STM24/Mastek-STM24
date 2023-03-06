import regex
from datetime import datetime

with open('vtt_transcrip.vtt', 'r') as f:
    vtt_lines = f.readlines()

timestamps = []
for line in vtt_lines:
    if regex.match(r'^\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}$', line.strip()):
        timestamps.append(line.strip())

formatted_timestamps = []
for ts in timestamps:
    start, end = ts.split(' --> ')
    start = datetime.strptime(start, '%H:%M:%S.%f')
    end = datetime.strptime(end, '%H:%M:%S.%f')
    formatted_timestamps.append((start, end))

# print(type(end))
# print(start,"----",end)
# print(formatted_timestamps)

lenn = len(formatted_timestamps) 
# print(formatted_timestamps[lenn - 1])

dt = formatted_timestamps[lenn - 1]

last_len = len(dt)

aaa = dt[last_len - 1]
aaa
minutes = aaa.minute

hours = aaa.hour

secs = aaa.second

print("Hours: ", hours)
print("Minutes: ", minutes)
print("Seconds: ", secs)

print(hours,"H:",minutes,"M:",secs,"S")