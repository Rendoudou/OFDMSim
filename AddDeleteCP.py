"""
@ OFDM仿真
@ 加入循环前缀
@ DD
"""

from GlobalParameter import *
import numpy as np


# #
# @ func def addCP(signal)::
# @ 添加循环前缀和循环后缀
# @ para array 复数信号
# @ return 添加结果
# #
def addCP(signal):
    ofdmNumber = signal.shape[0]  # 行数，获得ofdm符号的个数
    tempSignal = np.zeros((ofdmNumber, int(IFFTLength + GI + GIP)), complex)  # 生成复数空数组
    for i in range(ofdmNumber):
        for j in range(IFFTLength):  # 当傅里叶变换长度为512
            tempSignal[i, j + GI] = \
                signal[i, j]  # 第129 - 第640 用第1 - 第512个数据装填 0 - 511
            pass

        for j in range(GI):  # 0 - 127
            tempSignal[i, j] = \
                signal[i, int(j + IFFTLength - GI)]  # 添加循环前缀  第1 - 第128 用第385 - 第512个数据装填 384 - 511
            pass

        for j in range(GIP):  # 0 - 19
            tempSignal[i, int(IFFTLength + GI + j)] = signal[i, j]  # 添加循环后缀  前20个数据放到后面
            pass

    return tempSignal


# #
# @ func def deleteCP(signal)::
# @ 删除循环前缀和循环后缀
# @ para array 复数信号
# @ return 删除结果
# #
def deleteCP(signal):
    ofdmNumber = signal.shape[0]  # 行数，ofdm符号的个数
    temp = np.zeros((ofdmNumber, IFFTLength)).astype(complex)
    for i in range(ofdmNumber):
        temp[i] = signal[i, GI: GI + IFFTLength]  # 128 - 640 第 129 到 641,128 : 640

    return temp


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    a = np.zeros((3, 4))
    print(a.shape[0])
    pass
