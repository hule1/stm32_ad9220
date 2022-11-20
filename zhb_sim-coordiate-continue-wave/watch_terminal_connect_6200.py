# 功能：获取目标协调器的终端节点信息
# 方法：调用之前需将原始数据放置在“监视子节点最新动态/数据/”目录下
#       line96：txtfile = open("监视子节点最新动态/数据/mqtt1214_6200-2022-03-22.txt", "r+")
#       通过修改该txt文件来获取目标协调器的终端节点信息
# 作者：朱航彪
# 时间：2021/12/13

import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import reshape
import os

from pkg_resources import WorkingSet

def onetime(stattime, stoptime, oridata, macfiles):
    startstate = 0
    findmac = 0
    datamax = 0
    datamaxtemp = 0
    datamaxflag = 0
    mycnt = 0
    idcnt = 0
    tercnt = 0
    fullbuf = 0
    missedcnt = 0
    worktime = 0
    workperiod = 0
    windows = 0
    sleep = 0
    print(stattime)
    print("ID" + ":\t## recon_times " + " ## " +
          "data_length" + "\t## " + "length_max" + "\t##")
    if stattime.find("acad")!=-1:
        position = stattime.find("acad")
        workperiod = int(stattime[position+4:position+6],16)
        worktime = int(stattime[position+6:position+8],16)
        sleep = int(stattime[position+10:position+12],16)
        windows = int(stattime[position+12:position+14],16)

    for onemacfile in macfiles:
        txtmac = open(onemacfile)
        macdata = txtmac.readlines()
        for macline in macdata:
            tempmac = macline[:9]
            tempid = macline[29:34]

            for dataline in oridata:
                if dataline.find(stoptime) != -1:
                    if datamax < 14:
                        datamaxflag = datamax
                    if datamax == 14:
                        datamaxflag = "----"
                        fullbuf+=1
                    tercnt += 1
                    print(str(tempid) + ":  ##\t" +
                        str(idcnt) + "\t##\t" + str(datamax) + "\t##\t" + str(datamaxflag) + "\t##")
                    mycnt += idcnt
                    if idcnt == 0:
                        missedcnt+=1
                    idcnt = 0
                    datamax = 0
                    datamaxflag = 0
                    startstate = 0
                    break
                if dataline.find(stattime) != -1:
                    startstate = 1
                if startstate == 1:
                    if findmac == 1:
                        if dataline[37:41] == "abad":
                            position = dataline.find("abad")
                            cnttemp = dataline[position+1542:position+1544]
                            datamaxtemp = int(cnttemp, 16) + 1
                            if datamax < datamaxtemp:
                                datamax = datamaxtemp
                        if dataline[37:41] != "abad":
                            findmac = 0
                    if dataline.find(tempmac) != -1:
                        idcnt += 1
                        findmac = 1
    print("###\tworkperiod:\t"+str(int(workperiod/3))+" m\t###")
    print("###\tworktime:\t"+str(int(worktime/3))+" m\t###")
    print("###\tsleep:   \t"+str(sleep*10)+" s\t###")
    print("###\twindows:\t"+str(windows)+"\t###")
    print("###\trecved_buf:\t"+str(mycnt)+"\t###")
    print("###\tterminal_cnt\t"+str(tercnt)+"\t###")
    print("###\trecved_term\t"+str(tercnt-missedcnt)+"\t###")
    print("###\tfull_buf\t"+str(fullbuf)+"\t###")
    print("###\tfull_rate\t",end='')
    print("%.1f"%(100*fullbuf/(tercnt-missedcnt)),end='%')
    print("\t###")
    fullbuf = 0
    missedcnt = 0
    print(stoptime)


txtfile = open("监视子节点最新动态/数据/mqtt1214_6200-2022-03-22.txt", "r+")

macfile = "监视子节点最新动态/mac"  # 文件夹目录
macfiles = os.listdir(macfile)  # 得到文件夹下的所有文件名称
macs = []
for line in macfiles:  # 遍历文件夹
    position = macfile+'//' + line  # 构造绝对路径，"//"，其中一个'/'为转义符
    macs.append(position)
    print(position)

searchstarttime = " Wed Mar  9 19"
oridata = txtfile.readlines()

findstart = 0
findstop = 0
startsearch = 1  #该参数的使用需配合 searchstarttime 参数一起修改


for datalines in oridata:
    if (datalines.find(searchstarttime) != -1):
        startsearch = 1
    if startsearch == 1:
        if findstart == 1:
            if (datalines.find("2022   53544f50574f524b00") != -1):
                findstart = 0
                stoptime = datalines
                onetime(stattime, stoptime, oridata, macs)
        if datalines.find("2022   acad") != -1:
            findstart = 1
            stattime = datalines
