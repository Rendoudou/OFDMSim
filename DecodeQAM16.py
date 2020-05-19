"""
@ OFDM仿真
@ DecodeQAM16解调制
@ DD
"""

import numpy as np
from GlobalParameter import mapping, OFDMCarrierCount, Group, PilotInterval


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
# @ func: def getOfdmPosition()
# #
def getOfdmPosition():
    pos = np.zeros(Group * PilotInterval, int)
    for i in np.arange(Group):
        for j in np.arange(PilotInterval):
            pos[i * PilotInterval + j] = i * (PilotInterval + 1) + (j + 1)
        pass
    pass

    return list(pos)


# #
# @ func: def DecodeQAM16(fftSignalStream)
# @ 16QAM解调
# @ para 从高斯信道中接收的信号经过FFT
# @ return 解调后信息阵列
# #
def DecodeQAM16(signal):
    ofdmNumber = signal.shape[0]  # 一帧的符号数目,加入导频后是16
    signal_real_temp = signal.real.ravel()
    signal_imag_temp = signal.imag.ravel()

    if signal_real_temp.shape != signal_imag_temp.shape:
        print("OFDM仿真 ： error")
        return None

    length = OFDMCarrierCount * ofdmNumber
    if length != signal_real_temp.shape[0]:
        print("OFDM仿真 ： error")
        return None

    symbol16QAM = np.zeros((length, 2), int)  # 用作存储解码得到的16QAM符号（接收端）
    number_temp = np.zeros(length, int)
    bits_temp = np.zeros(length * 4, int)  # 用作存储解码得到的比特流（接收端）
    dis = []

    for i in np.arange(length):

        for j in np.arange(16):
            disTemp = (signal_real_temp[i] - mapping[str(j)][0]) ** 2 + \
                      (signal_imag_temp[i] - mapping[str(j)][1]) ** 2
            dis.append(disTemp)
            pass

        symbol16QAM[i] = mapping[str(dis.index(min(dis)))]  # 返回最小距离的坐标
        number_temp[i] = dis.index(min(dis))
        bits_temp[i * 4: i * 4 + 4] = toBits(dis.index(min(dis)))
        dis.clear()  # 列表清空，比较下一个符号
        pass

    # 在发送数据流中存在导频的时候
    pos = getOfdmPosition()
    number_out = (number_temp.reshape(ofdmNumber, -1))[pos]
    bits_out = (bits_temp.reshape(ofdmNumber, -1))[pos]
    return bits_out.ravel(), number_out.ravel()


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    pos = getOfdmPosition()
    print(pos)
    pass
