# 功能：绘制连续数据的波形
# 方法：调用之前需先启动ConnectWithTerminal.py程序
# 作者：朱航彪
# 时间：2022/03/25

from asyncio import futures
import pyqtgraph as pg
import array
import serial
import threading
import numpy as np
from queue import Queue
import time
import socket
import decoder

# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QFileDialog

pg.setConfigOption('background', 'w')

idxPlot = 0
state = 0
idx = 0
addr = []
cnt = []
data_raw = []
data_corrupt = False
data_done = False

q = Queue(maxsize=0)
r = Queue(maxsize=0)
s = Queue(maxsize=0)

BUFSIZE = 1280
ip_port = ('0.0.0.0', 42299)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp协议
server.bind(ip_port)

def Serial():
    global q, r, s
    global state
    global idx
    global addr
    global cnt1, cnt2
    global data_raw
    global data_corrupt, data_done
    fulldata = ""

    while (True):

        data2, client_addr = server.recvfrom(BUFSIZE)
        readdata = data2.hex()
        print(readdata)

        fulldata += readdata

        
        if fulldata[0:4]=="abad" and fulldata[-4:]=="aeae":
            xs,ys,zs, pacidx, err = decoder.decode(fulldata)

            for i in range(len(xs[0])):
                q.put(xs[0][i])
                r.put(ys[0][i])
                s.put(zs[0][i])
            fulldata = ""

        if fulldata[0:4] != 'abad':
            fulldata = ""

def plotData():
    global idxPlot

    if q.qsize() == 0:
        return

    if idxPlot < historyLength:
        data[idxPlot] = q.get()
        data2[idxPlot] = r.get()
        data3[idxPlot] = s.get()
        idxPlot = idxPlot + 1
    else:
        data[:-1] = data[1:]
        data[idxPlot - 1] = q.get()
        data2[:-1] = data2[1:]
        data2[idxPlot - 1] = r.get()
        data3[:-1] = data3[1:]
        data3[idxPlot - 1] = s.get()
    curve.setData(data)
    curve2.setData(data2)
    curve3.setData(data3)

def prr():
    global state
    if state>=2:
        state=0
    else:
        state+=1


if __name__ == "__main__":
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    app = pg.mkQApp()  # 建立app
    win = pg.GraphicsWindow()  # 建立窗口
    win.setWindowTitle(u'pyqtgraph逐点画波形图')
    win.resize(800, 500)  # 小窗口大小
    data = array.array('i')  # 可动态改变数组的大小,double型数组
    data2 = array.array('i')
    data3 = array.array('i')
    historyLength = 100  # 横坐标长度
    a = 0
    data = np.zeros(historyLength).__array__('d')  # 把数组长度定下来
    data2 = np.zeros(historyLength).__array__('d')
    data3 = np.zeros(historyLength).__array__('d')



    p = win.addPlot()  # 把图p加入到窗口中

    p.showGrid(x=True, y=True)  # 把X和Y的表格打开
    p.setRange(xRange=[0, historyLength], yRange=[-1000, 1000], padding=0)
    p.setLabel(axis='left', text='y / V')  # 靠左
    p.setLabel(axis='bottom', text='x / point')
    p.setTitle('semg')  # 表格的名字

    curve = p.plot(pen=pg.mkPen(width=5, color='r'))  # 绘制一个图形

    curve.setData(data)

    curve2 = p.plot(pen=pg.mkPen(width=5, color='g'))  # 绘制一个图形
    curve2.setData(data2)
    curve3 = p.plot(pen=pg.mkPen(width=5, color='y'))  # 绘制一个图形
    curve3.setData(data3)

    # proxy = QtGui.QGraphicsProxyWidget()
    # button = QtGui.QPushButton('button')
    # proxy.setWidget(button)

    # button.clicked.connect(prr) # 添加按钮监听

    # p3 = win.addLayout(row=2, col=0)
    # p3.addItem(proxy, row=1, col=1)


    # portx = 'COM7'
    # bps = 115200
    # # 串口执行到这已经打开 再用open命令会报错
    # mSerial = serial.Serial(portx, int(bps))
    # if (mSerial.isOpen()):
    #     print("open success")
    # else:
    #     print("open failed")
    #     serial.close()  # 关闭端口

    th1 = threading.Thread(target=Serial)
    th1.start()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(plotData)  # 定时刷新数据显示
    timer.start(1)  # 多少ms调用一次
    app.exec_()
