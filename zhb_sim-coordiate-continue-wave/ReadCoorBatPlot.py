# 功能：绘制连协调器的电压波形
# 方法：调用之前需将原始数据放置在“监视子节点最新动态/数据/”目录下
#       line12：fi = open("监视子节点最新动态/数据/mqtt1214_6200-2022-04-19.txt")
#       通过修改该txt文件来绘制不同节点不同时间段的电压
# 作者：朱航彪
# 时间：2021/12/13

from turtle import position
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

fi = open("监视子节点最新动态/数据/mqtt1214_6200-2022-04-19.txt")
data = fi.readlines()

start_time = "Fri Mar 11 12"
startflag = "5354415254574f524b00"
dataflag = "000000434f4f5244494e41544f525f3034"

start = 1
state = 1
coorbat = []
coortem = []
datatime = []

for lines in data:
    if lines.find(start_time) != -1:
        start = 1
    if start == 1:
        if state == 1:
            if lines.find(dataflag) != -1:
                temp = lines[83:87]
                template = lines[79:83]
                temp2 = int(temp, 16)
                template2 = int(template, 16)
                temp2 = temp2/4095*6.6
                template2 = (1.43-(template2*3.3/4096))/0.0043 + 25
                time = lines[21:26]
                if (temp2 < 4.2) & (temp2 > 3.2):
                    coorbat.append(temp2)
                    coortem.append(template2)
                    datatime.append(time)
                state = 1
# now time: Fri Mar 11 18: 38: 03 2022   00006b65001e1e8013002c1143313234010014027606b9085f0000000000434f4f5244494e41544f525f3034310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# now time: Fri Mar 11 20: 55: 39 2022   434f4f5244494e41544f525f303431005354415254574f524b00087006d8085c
        if lines.find(startflag) != -1:
            state = 1
            flagposition = lines.find(startflag)
            temp = lines[(flagposition + 28):(flagposition + 32)]
            template = lines[(flagposition + 24):(flagposition+28)]
            temp2 = int(temp, 16)
            template2 = int(template, 16)
            temp2 = temp2/4095*6.6
            template2 = (1.43-(template2*3.3/4096))/0.0043 + 25
            time = lines[21:26]
            if (temp2 < 4.2) & (temp2 > 3.2):
                coorbat.append(temp2)
                coortem.append(template2)
                datatime.append(time)


slip_num = int(len(datatime)/3)
plt.subplot(211)
x_values = datatime
y_values = coorbat
plt.plot(x_values, y_values, c='cornflowerblue')
plt.ylabel("Voltage")
x_major_locator = MultipleLocator(slip_num)
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.title("voltage and template waves one day")

plt.subplot(212)
x_values = datatime
y_values = coortem
plt.plot(x_values, y_values, c='orange')
x_major_locator = MultipleLocator(slip_num)
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.ylabel("Template")
plt.xlabel("time")
plt.show()
