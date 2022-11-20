import serial.tools.list_ports
import time
import serial

import xlwt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def disply_serial():
    """
        显示当前可用串口
    :return:
    """
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) <= 0:
        print("无串口设备")
    else:
        print("可用的串口设备如下：")
        for compont in ports_list:
            print(list(compont)[0], list(compont)[1])


def serial_init():
    disply_serial()
    # 默认波特率9600，8位数据位、1位停止位、0校验位
    ser = serial.Serial(port="COM5", baudrate=115200)
    ser.setDTR(False)
    ser.setRTS(False)
    if ser.isOpen():
        print("打开串口成功")
        print(ser.name)
    else:
        print("打开串口失败")
    return ser


def readline_serial(ser):
    com_input = ser.readline()
    com_input = com_input.decode()
    # print(type(com_input))
    # print()
    # if com_input:
    #     print(com_input)
    # else:
    #     ser.close()
    #     if ser.isOpen():
    #         print("串口未关闭")
    #     else:
    #         print("串口已关闭")
    return int(com_input)


def read_serial_duration(ser, second):
    begin = time.time()
    voltage = []
    while True:
        end = time.time()
        com_input = ser.readline()
        com_input = int(com_input.decode())
        voltage.append(com_input)
        if end - begin > second:
            ser.close()
            print("读取串口数据成功")
            break
    return voltage


def write_voltage_to_excel(list_voltage):
    f = xlwt.Workbook('encoding = utf-8')  # 设置工作簿编码
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)  # 创建sheet工作表
    # list1 = [1, 3, 4, 6, 8, 10]  # 要写入的列表的值
    for i in range(len(list_voltage)):
        sheet1.write(0, i, list_voltage[i])  # 写入数据参数对应 行, 列, 值
    f.save('text5.0.xls')  # 保存.xls到当前工作目录
    print("写入串口数据成功")


def draw_voltage_chart():
    ecg = pd.read_excel('text5.0.xls', header=None)
    plt.figure(figsize=(16, 8))
    ecg.iloc[0].plot()  # plot后不加.area就默认是折线图了;plot后加一个.area就是叠加区域图
    plt.title('voltage_chart' + str(0), fontsize=16, fontweight='bold')
    plt.ylabel('voltage', fontsize=12, fontweight='bold')
    plt.ylim(0, 4095)
    plt.xlabel('time/0.1s')
    plt.xticks(fontsize=8, rotation='45', ha='right')
    os.makedirs('voltage_chart', exist_ok=True)
    plt.savefig('voltage_chart/' + str(5), dpi=100)
    plt.show()
    plt.close()
    print("画图成功！")


if __name__ == '__main__':
    """
       单片机0.1秒发送一次实现功能读5秒数据然后退出
    """
    # ser = serial_init()
    # list_voltage = read_serial_duration(ser, 5)
    # print(list_voltage)
    # print(len(list_voltage))

    """
        测试画电压图
    """
    ser = serial_init()
    list_voltage = read_serial_duration(ser, 5)
    write_voltage_to_excel(list_voltage)
    draw_voltage_chart()
