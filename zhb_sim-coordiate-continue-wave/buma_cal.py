# 功能：差分数据还原
# 方法：
# 作者：袁建煊
# 时间：

import matplotlib.pyplot as plt


def hextoint4(strdata):
    tempp = int(strdata, 16)
    if (tempp & 0x8000 == 0x8000):
        return -((tempp - 1) ^ 0xFFFF)
    else:
        return tempp


def hextoint2(strdata):
    tempp = int(strdata, 16)
    if (tempp & 0x80 == 0x80):
        return -((tempp - 1) ^ 0xFF)
    else:
        return tempp


def chafen(ms):
    ns = []
    ns.append(hextoint4(ms[0][2:4] + ms[0][0:2]))
    for i in range(1, len(ms)):
        ns.append(ns[i - 1] + hextoint2(ms[i])*4)
    return ns


# if __name__ == '__main__':
# 0500
# 0b00
# 1501
# 000000
# 000000

# oridatas = 'abad02000001afaf00000800ff00010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101aeae'


def onebag(oridata):
    xs = []
    ys = []
    zs = []
    i = 0
    i += 16
    xs.append(oridata[i:i + 4])
    i += 4
    ys.append(oridata[i:i + 4])
    i += 4
    zs.append(oridata[i:i + 4])
    i += 4
    while oridata[i:i + 6] != '00aeae' and i < len(oridata) - 8:
        xs.append(oridata[i:i + 2])
        ys.append(oridata[i + 2:i + 2 + 2])
        zs.append(oridata[i + 2 + 2:i + 2 + 2 + 2])
        i += 6

    xss = chafen(xs)
    yss = chafen(ys)
    zss = chafen(zs)

    return xss, yss, zss


def threebag(oridatas):
    # oridatas = 'abad02000001afaf00000800ff00010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101aeae'
    oridatas = oridatas.split('aeae')
    xs = []
    ys = []
    zs = []
    for oridata in oridatas[:-1]:
        xt, yt, zt = onebag(oridata + 'aeae')
        xs.extend(xt)
        ys.extend(yt)
        zs.extend(zt)
    return xs, ys, zs


def poltbuma(oridata):
    xs, ys, zs = threebag(oridata)
    plt1 = plt.subplot(3, 1, 1)
    plt2 = plt.subplot(3, 1, 2)
    plt3 = plt.subplot(3, 1, 3)
    plt1.plot(xs)
    plt2.plot(ys)
    plt3.plot(zs)
    plt.show()


if __name__ == '__main__':
    threebag('123')

