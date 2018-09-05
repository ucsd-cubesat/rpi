import smbus        
import time         
import WirelessTool, colorama, traceback, led

mainServer = WirelessTool.TCPClient('127.0.0.1',3000,0.1)

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

time_old = int(time.time()*1000)
time_new = time_old+5000


def MPU_Init():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)  
        value = ((high << 8) | low)
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1)    
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

time.sleep(2)

while True:    
    try:
        if(time_new - time_old >= 5000):
            acc_x = read_raw_data(ACCEL_XOUT_H)
            acc_y = read_raw_data(ACCEL_YOUT_H)
            acc_z = read_raw_data(ACCEL_ZOUT_H)
        

            gyro_x = read_raw_data(GYRO_XOUT_H)
            gyro_y = read_raw_data(GYRO_YOUT_H)
            gyro_z = read_raw_data(GYRO_ZOUT_H)
            

            Ax = float("{0:.2f}".format(acc_x/16384.0))
            Ay = float("{0:.2f}".format(acc_y/16384.0))
            Az = float("{0:.2f}".format(acc_z/16384.0))
            
            Gx = float("{0:.2f}".format(gyro_x/131.0))
            Gy = float("{0:.2f}".format(gyro_y/131.0))
            Gz = float("{0:.2f}".format(gyro_z/131.0))
                
            bun = str(Ax)+','+str(Ay)+','+str(Az)+','+str(Gx)+','+str(Gy)+','+str(Gz)
  #          print bun
            mainServer.write('i1'+bun+'\t')
            time_old = time_new
            led.LED(2)
            time.sleep(1)
        else:
            time_new = int(time.time()*1000)  

    except BaseException as e:
        print(colorama.Fore.RED + '[ERROR]\t' + colorama.Style.RESET_ALL + e.message)
        print(colorama.Fore.RED + '[ERROR]\t' + colorama.Style.RESET_ALL + traceback.format_exc())
        mainServer.close()
        led.LED(4)
        break
