import os
import time
import csv
import io
from time import strftime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor='/sys/bus/w1/devices/28-0316a180c2ff/w1_slave'

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32
        return temp_c
    
while True:
    print(read_temp())
    text = str(read_temp())
    with open("temp.csv", 'a') as f:
        stamp = strftime('%B %d %Y, %I:%M %p')
        row = str(read_temp())
        w = csv.writer(f)
        w.writerow([row, stamp])
    time.sleep(600)

