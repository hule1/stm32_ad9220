# 功能：与子节点数据交互
# 方法：先将一个仅有LoRa模块的节点通过串口工具接入电脑，该LoRa模块用于接收终端节点数据，同时具备发送数据功能
#      该LoRa接收器应事先配置为目标终端节点的发送信道，该LoRa发送的数据由本程序提供
#      调用此程序之后，串口所连接的LoRa接收器可以持续获取终端节点的数据，并由该程序发送给绘图程序
# 作者：朱航彪
# 时间：2022/03/25

from time import sleep
import serial  # 导入模块
import socket
from sys import platform

# 00 1F 1F 77 6F 72 6B 00 1B 00 49 18 43 31 32 34 56 45 35 02 5E 02 00 00
# 77616b65 002222 8016004d1143313234 0d000d 0267
Addr = [0x00, 0x22, 0x22]
work = b"work"
mac = [0x80, 0x16, 0x00, 0x4d, 0x11, 0x43, 0x31, 0x32, 0x34, 0x4c, 0x00, 0x4c]
ctrl = [0x00, 0x5E, 0x02, 0x00, 0x00]
ackb = b"ackb"
num = [0x01]

send = []
msgposition = -1
wakemsg = 1
datamsg = 1

class workinst:   #定义一个类
    def _init_(self,addr,work,mac,ctrl):
        self.addr = addr
        self.work = work
        self.mac = mac
        self.ctrl = ctrl

class ackbinst:   #定义一个类
    def _init_(self,addr,ackb,mac,num):
        self.addr = addr
        self.ackb = ackb
        self.mac = mac
        self.num = num

def initSerial():
    # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
    if platform == "linux":
        portx = '/dev/ttyUSB0'
    elif platform == "win32":    
        portx = 'COM4'

    # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    bps = 115200
    # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    timex = 0.5
    # 打开串口，并得到串口对象
    ser = serial.Serial(portx, bps, timeout=timex)
    print("串口详情参数：", ser)

    print(ser.port)  # 获取到当前打开的串口名
    print(ser.baudrate)  # 获取波特率
    return ser

def checkResponse(ser, msg_send, msg_check="", retry=15):
    i = 0
    ser.write(msg_send)
    print("send: ", msg_send)
    while (i < retry):
        recv = ser.readline()
        print("receive: ", recv)
        if (len(recv) > 0 and recv[:len(msg_check)] == msg_check):
            return recv, False
        else:
            i += 1
    
    return recv, True

def initLora(ser):
    CPA_ADDR = b"AT+ADDR=37\r\n"
    CPA_CHEL = b"AT+CH=37\r\n"

    recv, timeout = checkResponse(ser, b"+++", b"a")
    if (timeout):
        return False
    
    recv, timeout = checkResponse(ser, b"a", b"+OK")
    if (timeout):
        return False

    recv, timeout = checkResponse(ser, CPA_ADDR, b"OK")
    if (timeout):
        return False

    recv, timeout = checkResponse(ser, CPA_CHEL, b"OK")
    if (timeout):
        return False

    recv, timeout = checkResponse(ser, b"AT+WMODE=FP\r\n", b"OK")
    if (timeout):
        return False

    recv, timeout = checkResponse(ser, b"AT+ENTM\r\n", b"OK")
    if (timeout):
        return False

    return True

myworkinst = workinst()
myackbinst = ackbinst()

myworkinst.addr = Addr
myworkinst.work = work
myworkinst.mac = mac
myworkinst.ctrl = ctrl

myackbinst.addr = Addr
myackbinst.ackb = ackb
myackbinst.mac = mac
myackbinst.num = num

try:
    ser = initSerial()
    success = initLora(ser)

    # 循环接收数据，此为死循环，可用线程实现

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_port = ('127.0.0.1', 42299)
    while True:
        if ser.in_waiting:
            recv =  ser.read(128)
            recv_data = recv.hex()
            print(recv_data)

            if recv_data.find("77616b65") != -1:
                # 十六进制的发送
                # print(Addr+work+mac+ctrl)
                msgposition = recv_data.find("77616b65")
                myworkinst.addr[0] = int(recv_data[msgposition + 8 : msgposition + 10],16)
                myworkinst.addr[1] = int(recv_data[msgposition + 10 : msgposition + 12],16)
                myworkinst.addr[2] = int(recv_data[msgposition + 12 : msgposition + 14],16)
                for i in range(12):
                    myworkinst.mac[i] = int(recv_data[msgposition + 14 + 2*i: msgposition + 16 + 2*i],16)

                ser.write(myworkinst.addr)  # 写数据
                ser.write(myworkinst.work)  # 写数据
                ser.write(myworkinst.mac)  # 写数据
                ser.write(myworkinst.ctrl)  # 写数据
            elif recv_data.find("abad00") != -1:
                ser.write(myackbinst.addr)  # 写数据
                ser.write(myackbinst.ackb)  # 写数据
                ser.write(myackbinst.mac)  # 写数据
                ser.write(myackbinst.num)  # 写数据
                client.sendto(recv, ip_port)
            else:
                client.sendto(recv, ip_port)
        else:
            sleep(0.5)
            
    print("---------------")
    ser.close()  # 关闭串口
    client.close()

except Exception as e:
    print("---异常---：", e)