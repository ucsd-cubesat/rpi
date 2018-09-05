import WirelessTool, socket, traceback, colorama, time, led
colorama.init()

data_send = [0,0,0,0] 

mainServer = WirelessTool.TCPEchoServer(3000,0.1)
while(not mainServer.connect(10)):
    print(colorama.Fore.YELLOW + '[INFO]\t' + colorama.Style.RESET_ALL + "Waiting Subprocess 1 Connection")

while(not mainServer.connect(10)):
    print(colorama.Fore.YELLOW + '[INFO]\t' + colorama.Style.RESET_ALL + "Waiting Subprocess 2 Connection")

while(not mainServer.connect(10)):
    print(colorama.Fore.YELLOW + '[INFO]\t' + colorama.Style.RESET_ALL + "Waiting Subprocess 2 Connection")

def decodeCommand(rawData):
    recvLength = len(rawData)
    if(recvLength < 1):
        return [('Z', 0, '0')]
    else:
        rawData = rawData.split('\t')
        dataList = []
        for element in rawData:
            if(len(element) == 0): # Handles the extra '' sometime when spliting
                continue
            elif(element == 'Z'):
                return [('Z', 0, '0')]
            elif(element[0] == 't'): # Temperature sensor
                dataList.append((element[0], int(element[1]), element[2:]))
            elif(element[0] == 'i'): #imu
                dataList.append((element[0],int(element[1]),element[2:])) 
            else:
                print('[ERROR]\tUnexpected command received:->' + element + '<-')
        return dataList

def decodeList(rawDataList):
    dataList = [('Z', 0, '0')]
    for dataPacket in rawDataList:
        dataPacket = dataPacket.split('\t')
        for element in dataPacket:
            if(len(element) == 0): # Handles the extra '' sometime when spliting
                continue
            elif(element == 'Z'):
                continue
            elif(element[0] == 't'): # Temperature sensor
                dataList.append((element[0], int(element[1]), element[2:]))
            elif(element[0] == 'i'): #imu
                dataList.append((element[0],int(element[1]),element[2:])) 
            else:
                print('[ERROR]\tUnexpected command received:->' + element + '<-')
    return dataList

mainServer.readAll()
while(True):
    try:
        x = 0
        tempDataRaw = mainServer.readAll()
        # print(tempDataRaw)
        for dataType,index,data in decodeList(tempDataRaw):
            if(dataType == 'Z'):
                pass
 		led.LED(4)
            elif(dataType == 't' and index == 1):
		led.LED(3)
                data_send[0] = data
              #  print(colorama.Fore.GREEN + '[TEMP1]\t' + colorama.Style.RESET_ALL + data)
            elif(dataType == 't' and index == 2):
		led.LED(3)
		data_send[1] = data
              #  print(colorama.Fore.GREEN + '[TEMP2]\t' + colorama.Style.RESET_ALL + data)
            elif(dataType == 't' and index == 3):
		led.LED(3)
		data_send[2] = data
              #  print(colorama.Fore.GREEN + '[TEMP3]\t' + colorama.Style.RESET_ALL + data)
            elif(dataType == 'i'):
		led.LED(3)
		data_send[3] = data
              #  print(colorama.Fore.BLUE + '[IMU]\t' + colorama.Style.RESET_ALL + data)
           

            if(data_send[0] != 0 and data_send[1]!= 0 and data_send[2]!= 0 and data_send[3] != 0):
		print data_send[0]+','+data_send[1]+','+data_send[2]+','+data_send[3] 
                data_str = data_send[0]+','+data_send[1]+','+data_send[2]+','+data_send[3]+'\n'
                mainServer.writeClient(2,data_str)
                time.sleep(1)

    except BaseException as e:
        print(colorama.Fore.RED + '[ERROR]\t' + colorama.Style.RESET_ALL + e.message)
        print(colorama.Fore.RED + '[ERROR]\t' + colorama.Style.RESET_ALL + traceback.format_exc())
        mainServer.close()
        led.LED(4)
        break
