import numpy as np

def hextoint4(strdata, little_endian=True):
    data = ''.join(strdata)
    if (little_endian):
        tempp = int(data[2:4] + data[0:2], 16)
    else:
        tempp = int(data, 16)

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

codebook = {'f': '0', 'd': '1', 'e': '2', 'c': '3', '7': '4', '5': '5', '6': '6', '4': '7', 'b': '8', '9': '9',
            'a': 'a', '8': 'b', '3': 'c', '1': 'd', '2': 'e', '0': 'f'}

def calxyzs(xyzdata):
    inx = 12
    strdata = []
    for i in range(inx, len(xyzdata) - 4):
        strdata.append(codebook[xyzdata[i]])

    data = []
    for i in range(20*3):
        data.append(hextoint4(strdata[i*4:(i+1)*4]))

    xs = data[0::3]
    ys = data[1::3]
    zs = data[2::3]

    return xs, ys, zs

def calxyzs_diff(xyzdata):
    xs, ys, zs = calxyzs(xyzdata)

    xsd = [xs[0]]
    ysd = [ys[0]]
    zsd = [zs[0]]
    for i in range(1, len(xs)):
        xsd.append(xsd[i-1] + int((xs[i] - xs[i-1])/4)*4)
        ysd.append(ysd[i-1] + int((ys[i] - ys[i-1])/4)*4)
        zsd.append(zsd[i-1] + int((zs[i] - zs[i-1])/4)*4)
    
    return xsd, ysd, zsd


def onebag(oridata, factor=1):
    data = []
    for i in range(3):
        data.append(hextoint4(oridata[i*4 + 16:(i+1)*4 + 16]))
    for i in range(37*3):
        data.append(hextoint2(oridata[i*2 + 28:(i+1)*2 + 28])*factor)
    
    xs = np.cumsum(data[0::3])
    ys = np.cumsum(data[1::3])
    zs = np.cumsum(data[2::3])

    return xs, ys, zs

def onebag2(oridata, factor=1):
    l = len(oridata) - 4
    idx = 16
    xs = [hextoint4(oridata[idx:idx+4], little_endian=False)]
    ys = [hextoint4(oridata[idx+4:idx+8], little_endian=False)]
    zs = [hextoint4(oridata[idx+8:idx+12], little_endian=False)]
    idx += 12

    disMode = True
    while(idx < l-1):
        if disMode:
            if (hextoint2(oridata[idx:idx+2]) == 127):
                disMode = False
                idx += 6
            else:
                if (idx < l-6):
                    xs.append(xs[-1] + hextoint2(oridata[idx:idx+2]))
                    ys.append(ys[-1] + hextoint2(oridata[idx+2:idx+4]))
                    zs.append(zs[-1] + hextoint2(oridata[idx+4:idx+6]))
                idx += 6
        else:
            if (hextoint2(oridata[idx:idx+2]) == -128):
                disMode = True
                idx += 6
            else:
                if (idx < l-12):
                    xs.append(hextoint4(oridata[idx:idx+4], little_endian=False))
                    ys.append(hextoint4(oridata[idx+4:idx+8], little_endian=False))
                    zs.append(hextoint4(oridata[idx+8:idx+12], little_endian=False))
                idx += 12
    return xs, ys, zs

def decode(oridatas):
    xs = []
    ys = []
    zs = []
    pacidx = []
    e = [0, 0]

    data_process = oridatas
    while (True):
        idx = data_process.find('abad')
        if (idx == -1):
            break

        data_process = data_process[idx:]
        if (len(data_process) < 256):
            break
        
        data = data_process[:256]
        data_process = data_process[256:]

        if (data[252:256] != 'aeae'):
            e[0] += 1
            continue

        if (data[12:16] == 'afaf'):
            xt, yt, zt = onebag(data, 4)
        elif (data[12:16] == 'afbf'):
            xt, yt, zt = onebag2(data, 1)
        else:
            if (data.find('010301030103') == -1):
                xt, yt, zt = calxyzs_diff(data)
            else:
                e[1] += 1
                continue

        xs.append(xt)
        ys.append(yt)
        zs.append(zt)

        pacidx.append(int(data[10:12], 16))

    err = ''
    if e[0] != 0:
        err += '\tno aeae ' + str(e[0])
    if e[1] != 0:
        err += '\t0103 ' + str(e[1])

    return xs, ys, zs, pacidx, err
