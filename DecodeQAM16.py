"""
@ OFDM仿真
@ DecodeQAM16解调制
@ DD
"""

from GlobalParameter import mapping
import numpy as np
from GlobalParameter import OFDMCarrierCount


# #
# @ func: def toBits(x): 16QAM
# @ 10进制转2进制
# @ para 10进制数
# @ return 2进制数据数组
# #
def toBits(x):
    bits = np.zeros(4)
    temp = list(bin(x))
    for i in np.arange(4):
        if temp[-i - 1] == 'b':
            bits[i] = 0
            break
        else:
            bits[i] = temp[-i - 1]
            pass
        pass

    return bits


# #
# @ func: def DecodeQAM16(fftSignalStream)
# @ 16QAM解调
# @ para 从高斯信道中接收的信号经过FFT
# @ return 解调后信息阵列
# #
def DecodeQAM16(signal_real, signal_imag):
    ofdmNumber = signal_real.shape[0]
    signal_real_temp = signal_real[0: ofdmNumber, 0: OFDMCarrierCount].ravel()
    signal_imag_temp = signal_imag[0: ofdmNumber, 0: OFDMCarrierCount].ravel()

    if signal_real_temp.shape != signal_imag_temp.shape:
        print("OFDM仿真 ： error")
        return None

    length = OFDMCarrierCount * ofdmNumber
    if length != signal_real_temp.shape[0]:
        print("OFDM仿真 ： error")
        return None

    symbol16QAM = np.zeros((length, 2))  # 用作存储解码得到的16QAM符号（接收端）
    number16QAM = np.zeros(length)
    bitsOut = np.zeros(length * 4)  # 用作存储解码得到的比特流（接收端）
    dis = []

    for i in np.arange(length):

        for j in np.arange(16):
            disTemp = (signal_real_temp[i] - mapping[str(j)][0]) ** 2 + \
                      (signal_imag_temp[i] - mapping[str(j)][1]) ** 2
            dis.append(disTemp)
            pass

        symbol16QAM[i] = mapping[str(dis.index(min(dis)))]  # 返回最小距离的坐标
        number16QAM[i] = dis.index(min(dis))
        bitsOut[i * 4: i * 4 + 4] = toBits(dis.index(min(dis)))
        dis.clear()  # 列表清空，比较下一个符号
        pass

    # print(type(bitsOut))
    # print(type(bitsOut.astype(int)))
    bitsOut = bitsOut.astype(int)
    return bitsOut, number16QAM


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    liatT = [1, 2, 3, 4]

    print(liatT.index(2))

    a = bin(10)
    b = list(a)
    c = np.zeros((3, 4))

    print(c)
    pass
