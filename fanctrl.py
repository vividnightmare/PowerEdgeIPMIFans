#
##########
#
#   Manually Control Fan Speeds on Dell PowerEdge
#
#   Sometimes you get that sweet iDRAC that doesnt work
#   Actually I bet this happens more than Dell wants to admit
#
#   Tested on R620 and R210 II
#   Requires ipmitool
#
##########
#


import os
import time
import psutil


#####
#   our fan curve
#   TempC : Fan%
#####
curve = {80 : 100,
         75 : 75,
         70 : 65,
         65 : 45,
         60 : 35,
         55 : 30,
         50 : 25,
         0 : 15
}


def enable_manual_control():
    cmd = "ipmitool raw 0x30 0x30 0x01 0x00 >/dev/null"
    os.system(cmd)
    return 0


def disable_manual_control():
    cmd = "ipmitool raw 0x30 0x30 0x01 0x01 >/dev/null"
    os.system(cmd)
    return 0


def set_fan_speed(speed):
    speed = hex(speed)
    cmd = "ipmitool raw 0x30 0x30 0x02 0xff " + speed + " 2>/dev/null"
    os.system(cmd)
    return 0


def set_single_fan_speed(fan, speed):
    fan = hex(fan)
    speed = hex(speed)
    cmd = "ipmitool raw 0x30 0x30 0x02 " + fan + " " + speed + " 2>/dev/null"
    os.system(cmd)
    return 0


def get_cpu_temp():
    temp = psutil.sensors_temperatures()
    cpu_temp = []
    for name, entries in temp.items():
        for entry in entries:
            cpu_temp.append(entry.current)
    high_temp = max(cpu_temp)
    return high_temp


enable_manual_control()


set_fan_speed(15)


print("----------")


while True:
    temp = get_cpu_temp()
    print("Temp: " + str(temp) + "C")
    for entry in curve:
        if temp >= entry:
            set_fan_speed(curve[entry])
            print("Fans: " + str(curve[entry]) + "%")
            break
    print("----------")
    time.sleep(5)

    
exit(0)
