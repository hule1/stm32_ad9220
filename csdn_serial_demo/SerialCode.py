# -*- coding=UTF-8 -*-

# 第三方库导入，记得需要多导入pyserial这个第三方库
import sys
import numpy
import serial
from PyQt5 import QtWidgets
import threading
import matplotlib.ticker as ticker
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.dates import date2num
import numpy as np
from matplotlib.figure import Figure
import os
import csv
import time

# 串口打开,根据需要自行修改串口号，波特率
# ser = serial.Serial()
# ser.baudrate = 115200
# ser.port = 'COM8'
# print(ser)
# ser.open()
# print(ser.is_open)


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.curveObj = None

    def plot(self, datax, datay):
        if self.curveObj is None:
            self.curveObj, = self.ax.plot_date(np.array(datax), np.array(datay), 'b-')

        else:
            self.curveObj.set_data(np.array(datax), np.array(datay))
            self.ax.set_xlim(datax[0], datax[-1])


            # 这是纵坐标轴的范围，可根据需要自行修改
            self.ax.set_ylim(99, 101)
            self.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))

        xticklabels = self.ax.xaxis.get_ticklabels()
        for xtick in xticklabels:
            xtick.set_rotation(25)

        yticklabels = self.ax.yaxis.get_ticklabels()
        for ytick in yticklabels:
            ytick.set_rotation(1.0)

        self.draw()



class Window(QtWidgets.QWidget):
    flag = 1
    count = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = MplCanvas()

        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button
        self.button1 = QtWidgets.QPushButton('StartPlot')
        self.button1.clicked.connect(self.startplot)

        self.button2 = QtWidgets.QPushButton('Zoom')
        self.button2.clicked.connect(self.zoom)

        self.button3 = QtWidgets.QPushButton('Pan')
        self.button3.clicked.connect(self.pan)

        self.button4 = QtWidgets.QPushButton('Home')
        self.button4.clicked.connect(self.home)

        self.button5 = QtWidgets.QPushButton('Save')
        self.button5.clicked.connect(self.save)

        self.button6 = QtWidgets.QPushButton('Clear')
        self.button6.clicked.connect(self.clear)

        self.button7 = QtWidgets.QPushButton('StopPlot')
        self.button7.clicked.connect(self.stopplot)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)


        btnlayout = QtWidgets.QHBoxLayout()
        btnlayout.addWidget(self.button1)
        btnlayout.addWidget(self.button2)
        btnlayout.addWidget(self.button3)
        btnlayout.addWidget(self.button4)
        btnlayout.addWidget(self.button5)
        btnlayout.addWidget(self.button6)
        btnlayout.addWidget(self.button7)

        self.dataX = []
        self.dataY = []
        self.dataX2 = []
        self.dataY2 = []


        qw = QtWidgets.QWidget(self)
        qw.setLayout(btnlayout)
        layout.addWidget(qw)
        self.setLayout(layout)

    def getdata(self):
        return numpy.array([i for i in range(100)])

    def home(self):
        self.toolbar.home()
        self.toolbar2.home()

    def zoom(self):
        self.toolbar.zoom()
        self.toolbar2.zoom()

    def pan(self):
        self.toolbar.pan()
        self.toolbar2.pan()

    def save(self):
        self.toolbar.save_figure()

    def startplot(self):
        ''' plot some random stuff '''
        self.tData = threading.Thread(name="dataGenerator", target=self.generateData)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.tData.start()

    def stopplot(self):
        if Window.flag == 1:
            Window.flag = -2
            self.__running.clear()
        else:
            Window.flag = 1
            self.__running.set()

    def generateData(self):
        # 在当前文件夹下创建保存数据的csv文件
        self.Now_Time = str(datetime.now())[:10]
        if not os.path.exists('./data'):
            os.mkdir('./data')
        if not os.path.exists('./data/DataFile'):
            os.mkdir('./data/DataFile')
            with open('./data/DataFile/{time}.csv'.format(time=self.Now_Time), 'a+', newline='') as f1:
                writer1 = csv.DictWriter(f1, ['Time', 'Data'])
                writer1.writeheader()
        while 1:
            if self.__running.isSet():
                # 串口读取数据，数据的读取和解析需要自己改写,然后将输出值传递给s
                # s = ser.readline()

                s=100
                newTime = date2num(datetime.now())
                self.dataX.append(newTime)
                self.dataY.append(s)
                self.canvas.plot(self.dataX, self.dataY)


                # 将数据保存到文件中去
                with open('./data/DataFile/{time}.csv'.format(time=self.Now_Time), 'a+', newline='') as f2:
                    writer2 = csv.writer(f2)
                    writer2.writerow([str(datetime.now())[11:], str(s)])
                time.sleep(0.5)

    def clear(self):
        self.axes.cla()
        self.axes.set_xlabel('Frequency')
        self.axes.set_ylabel('Amplification')
        self.axes.set_title('test')
        self.tData.join()
        self.canvas.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.setWindowTitle('Simple QTpy and MatplotLib example with Zoom/Pan')
    main.show()
    sys.exit(app.exec_())
