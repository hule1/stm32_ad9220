# 功能：绘制某协调器下属的，某天的，终端节点电压情况
# 方法：调用之前需将原始数据放置在“监视子节点最新动态/数据/”目录下
#       注意：以下三行根据实际需要进行更改
#
#           txtfile41 = open("年后测试/mqtt1214_2241-2022-02-28.txt", "r+")
#           txtfile61 = open("监视子节点最新动态/数据/mqtt1214_6200-2022-03-18.txt", "r+")
#           oridata = txtfile61.readlines()
#
# 作者：朱航彪
# 时间：2021/02/10


import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import reshape
import os

datafile = "监视子节点最新动态/数据"  # 文件夹目录
datafiles = os.listdir(datafile)  # 得到文件夹下的所有文件名称
macfile = "监视子节点最新动态/mac"  # 文件夹目录
macfiles = os.listdir(macfile)  # 得到文件夹下的所有文件名称

datafiles.sort(key=lambda x: int(x[-6:-4]), reverse=True)

txts = []
macs = []

for line in datafiles:  # 遍历文件夹
    position = datafile+'//' + line  # 构造绝对路径，"//"，其中一个'/'为转义符
    txts.append(position)
    print(position)

for line in macfiles:  # 遍历文件夹
    position = macfile+'//' + line  # 构造绝对路径，"//"，其中一个'/'为转义符
    macs.append(position)
    print(position)

txtfile41 = open("年后测试/mqtt1214_2241-2022-02-28.txt", "r+")
txtfile61 = open("监视子节点最新动态/数据/mqtt1214_6200-2022-03-18.txt", "r+")

oridata = txtfile61.readlines()

adc = []

t = 0
adcposition = 0
id = 0

for macfile in macs:
    macdata = open(macfile).readlines()
    for macline in macdata:
        tempmac = macline[:9]
        tempid = macline[29:34]
        adcposition = t
        id += 1
        for dataline in oridata:
            position = dataline.find(tempmac)
            if position != -1:
                temp = dataline[position+24:position+28]
                Senser = dataline[position+29:position+33]
                temp2 = int(temp, 16)
                if (temp2 < 1024) & (temp2 > 500):
                    temp2 = 1024*2.5/temp2
                    adc.append(temp2)
                    t += 1
        plt.subplot(8, 10, id)
        plt.ylim((3.3, 4.3))
        plt.title(id)
        plt.plot(adc[adcposition:])

plt.show()

# break
