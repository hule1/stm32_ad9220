import array
import serial
import threading
import numpy as np
import time
import pyqtgraph as pg

i = 0


def Serial():
    while (True):
        n = mSerial.inWaiting()
        if (n):
            if data != " ":
                dat =int(mSerial.readline(4).decode())
                # dat = int.from_bytes(a, byteorder='little')  # 格式转换
                # print(type(dat))
                n = 0
                global i;
                if i < historyLength:
                    data[i] = dat
                    i = i + 1
                else:
                    data[:-1] = data[1:]
                    data[i - 1] = dat


def plotData():
    curve.setData(data)


if __name__ == "__main__":
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    app = pg.mkQApp()  # 建立app
    win = pg.GraphicsWindow()  # 建立窗口
    win.setWindowTitle(u'pyqtgraph逐点画波形图')
    win.resize(800, 500)  # 小窗口大小
    # win.setBackground('w')
    data = array.array('i')  # 可动态改变数组的大小,double型数组
    historyLength = 200  # 横坐标长度
    a = 0
    data = np.zeros(historyLength).__array__('d')  # 把数组长度定下来
    p = win.addPlot()  # 把图p加入到窗口中
    p.showGrid(x=True, y=True)  # 把X和Y的表格打开
    p.setRange(xRange=[0, historyLength], yRange=[-4095, 4095], padding=0)
    p.setLabel(axis='left', text='y / V')  # 靠左
    p.setLabel(axis='bottom', text='x / point')
    p.setTitle('电压波形图')  # 表格的名字

    curve = p.plot(pen=pg.mkPen(width=3, color='g'))  # 绘制一个图形
    curve.setData(data)
    portx = 'COM5'
    bps = 115200
    # 串口执行到这已经打开 再用open命令会报错
    mSerial = serial.Serial(portx, int(bps))
    if (mSerial.isOpen()):
        print("open success")
        mSerial.write("hello".encode())  # 向端口些数据 字符串必须译码
        mSerial.flushInput()  # 清空缓冲区
    else:
        print("open failed")
        serial.close()  # 关闭端口
    th1 = threading.Thread(target=Serial)  # 装饰器 目标函数一定不能带（）被这个BUG搞了好久
    th1.start()
    timer = pg.QtCore.QTimer() # 实例化定时器
    timer.timeout.connect(plotData)  # 定时刷新数据显示
    timer.start(1)  # 多少ms调用一次
    app.exec_()
