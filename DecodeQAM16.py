"""
@ OFDM仿真
@ DecodeQAM16解调制
@ DD
"""

from GlobalParameter import mapping
import numpy as np


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
def DecodeQAM16(signal_i, signal_q):

    if signal_i.shape[0] != signal_q.shape[0]:
        print("OFDM仿真 ： error")
    length = signal_i.shape[0]
    symbol16QAM = np.zeros((length, 2))  # 用作存储解码得到的16QAM符号（接收端）
    bitsOut = np.zeros(length * 4)  # 用作存储解码得到的比特流（接收端）
    dis = []

    for i in np.arange(length):

        for j in np.arange(16):
            disTemp = (signal_i[i] - mapping[str(j)][0]) ** 2 + (signal_q[i] - mapping[str(j)][1]) ** 2
            dis.append(disTemp)
            pass

        symbol16QAM[i,] = mapping[str(dis.index(min(dis)))]
        bitsOut[i * 4: i * 4 + 4] = toBits(dis.index(min(dis)))
        dis.clear()  # 列表清空，比较下一个符号
        pass

    # print(type(bitsOut))
    # print(type(bitsOut.astype(int)))
    bitsOut = bitsOut.astype(int)
    return bitsOut


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    a = bin(10)
    b = list(a)
    c = np.zeros((3, 4))

    print(c)
    pass