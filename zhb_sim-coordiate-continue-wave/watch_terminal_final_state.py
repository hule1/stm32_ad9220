# 功能：获取所有协调器的所有终端节点信息
# 方法：调用之前需将原始数据放置在“监视子节点最新动态/数据/”目录下
#       注意，数据文件最好不要跨月份，函数中没用对月份的判断
# 作者：朱航彪
# 时间：2021/02/10

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


def strtochr(strdata):
    hex = []
    length = len(strdata)
    for i in range(0, length, 2):
        temp = int(strdata[i:i+2], 16)
        hex.append(chr(temp))
    list2 = [str(i) for i in hex]  # 使用列表推导式把列表中的单个元素全部转化为str类型
    list3 = ''.join(list2)  # 把列表中的元素放在空串中，元素间用空格隔开
    return list3  # 查看生成的长串


def newest(data1, data2):
    if int(data1[18:20], 16) > int(data2[18:20], 16):
        return data1
    elif int(data1[18:20], 16) < int(data2[18:20], 16):
        return data2
    elif int(data1[18:20], 16) == int(data2[18:20], 16):
        if int(data1[21:23], 16) > int(data2[21:23], 16):
            return data1
        elif int(data1[21:23], 16) < int(data2[21:23], 16):
            return data2
        elif int(data1[21:23], 16) == int(data2[21:23], 16):
            if int(data1[24:26], 16) > int(data2[24:26], 16):
                return data1
            else:
                return data2

# now time: Wed Mar  9 00: 49: 21 2022   00006b65001d1d001a0022184331323401000c027606d108b40000000000434f4f5244494e41544f525f30343000000
# now time: Wed Mar  9 10: 16: 08 2022   00006b65001d1d001a0052184331323409001d0275069c091b0000000000434f4f5244494e41544f525f3034300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000


def printlastmes_in_data(mac, id, dataline):

    position = dataline.find(mac)
    if position != -1:
        print(str(id) + " latest state: ", end=" ")
        print("time: " + str(dataline[18:36]), end=" #  ")
        position = dataline.find("434f4f5244494e41544f525")
        coordiator = strtochr(dataline[position:position+31])
        print("coordiator: " + str(coordiator), end=" #  ")
        position = dataline.find(mac)
        temp = dataline[position+24:position+28]
        temp2 = int(temp, 16)
        temp2 = 1024*2.5/temp2
        print("voltage: %.2f" % temp2)


findmesflag = 0
# temmac = "001a00521843"
# temid = "29-8 "
olddata = "now time: Wed Mar  6 10:16:08 2022   00006b65001d1d001a0052184331323409001d0275069c091b0000000000434f4f5244494e41544f525f3034300000000000"
newestdata = olddata
# printlastmes_in_data(temmac, temid, temdata)
# newest(temdata, temdata)

for onemacfile in macs:
    txtmac = open(onemacfile)
    macdata = txtmac.readlines()
    for macline in macdata:
        tempmac = macline[:9]
        tempid = macline[29:34]
        for onedatafile in txts:
            txtdata = open(onedatafile)
            oridata = txtdata.readlines()
            for dataline in oridata[::-1]:
                if dataline.find(tempmac) != -1:
                    findmesflag = 1
                    newestdata = newest(newestdata, dataline)
                    break
            # if findmesflag == 1:
            #     break
        if findmesflag == 1:
            printlastmes_in_data(tempmac, tempid, newestdata)
        else:
            print(str(tempid) + " no data ")
        findmesflag = 0
        newestdata = olddata
