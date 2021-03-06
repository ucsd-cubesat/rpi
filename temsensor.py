import os
import glob
import time
import WirelessTool, colorama, traceback, led


mainServer = WirelessTool.TCPClient('127.0.0.1',3000,0.1)


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-011832501aff')[0]
device_file = device_folder + '/w1_slave'

device_folder1 = glob.glob(base_dir + '28-01183254a6ff')[0]
device_file1 = device_folder1 + '/w1_slave'

device_folder2 = glob.glob(base_dir + '28-0118326173ff')[0]
device_file2 = device_folder2 + '/w1_slave'

time_old = int(time.time()*1000)#millis 
time_new = time_old+5000


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw1():
    f = open(device_file1, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw2():
    f = open(device_file2, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def read_temp1():
    lines = read_temp_raw1()
    while lines[0].strip()[-3:] != 'YES':
        lines = read_temp_raw1()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def read_temp2():
    lines = read_temp_raw2()
    while lines[0].strip()[-3:] != 'YES':
        lines = read_temp_raw2()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c



while True:
    try:
        if(time_new - time_old >= 5000):    
            t1 = str(read_temp())
            print('temp1 sent = ' + t1)
            mainServer.write('t1' + t1 + '\t')
            t2 = str(read_temp1())
            print 'temp2 sent = ' + t2
            mainServer.write('t2' + t2 + '\t')
            t3 = str(read_temp2())
            print 'temp3 sent = '+ t3
            mainServer.write('t3' + t3 + '\t')
            time_old = time_new
            led.LED(1)
        else:
            time_new = int(time.time()*1000)
           
      
    except BaseException as e:
        print(colorama.Fore.RED + '[ERROR]\t' + colorama.Style.RESET_ALL + e.message)
        print(colorama.Fore.RED + '[ERROR]\t' + colorama.Style.RESET_ALL + traceback.format_exc())
        mainServer.close()
        led.LED(4)
        break
