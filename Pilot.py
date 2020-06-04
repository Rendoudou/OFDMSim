"""
@ OFDM仿真
@ OFDM系统信道估计 加入导频
@ DD
@ 参考博客 https://zhuanlan.zhihu.com/p/57967971
"""

import numpy as np
from QAM16 import qam16
from GlobalParameter import OFDMCarrierCount, SymbolPerCarrier, BitsPerSymbol, PilotInterval, mapping

# 静态变量
pilotsNeed = int(SymbolPerCarrier / PilotInterval)  # 导频需要的行数，实质信息行数除以导频间的信息间隔
pilots = np.zeros((pilotsNeed, OFDMCarrierCount), complex)  # 存储生成的导频
labels_2_classification = np.zeros((pilotsNeed, OFDMCarrierCount, 2), int)  # 记录大致象限
labels_16_classification = np.zeros(pilotsNeed * OFDMCarrierCount, int)
pilotsPos = np.zeros(pilotsNeed, int)  # 块状导频的位置
basic_0 = int('0')


#
# 块状导频需要的预设导频符号流
#
def creatPilot():
    bits = np.random.randint(0, 2, OFDMCarrierCount * BitsPerSymbol)
    [agjustedSymbol, numbers] = qam16(bits)

    return np.array(agjustedSymbol)  # 返回一个已知的导频复数数组


#
# 块状导频需要的预设导频符号流
#
def getLabel_2_classification(symbol):
    n = len(symbol)
    posi = np.zeros((n, 2))
    for i in np.arange(n):
        if symbol[i].real >= 0:
            posi[i, 0] = 1
            pass
        else:
            posi[i, 0] = 0
            pass

        if symbol[i].imag >= 0:
            posi[i][1] = 1
            pass
        else:
            posi[i][1] = 0
            pass
        pass

    return posi


#
# 字典通过value 返回键值 get_key(dict, value):
#
def get_key(dict_search, value):
    return [k for k, v in dict_search.items() if v == value]


#
# getLabel_16_classification
#
def getLabel_16_classification(symbol):
    labels = np.zeros(OFDMCarrierCount, int)  # 每次解析一行
    for i in np.arange(OFDMCarrierCount):
        labels[i] = int((get_key(mapping, [symbol[i].real, symbol[i].imag]))[0]) - basic_0
    return labels


#
# 块状导频需要的预设比特流
#
def insertPilot(qamStream):
    symbolMatrix = np.array(qamStream).reshape((-1, OFDMCarrierCount))  # n行，列为ofdm信号的长度
    matrixWithPilots = np.zeros((SymbolPerCarrier + pilotsNeed, OFDMCarrierCount), complex)  # 新建空数组空间用于存储加入导频的符号帧

    for i in np.arange(pilotsNeed):  # 0 - 3 插入符号
        pilots[i, :] = creatPilot()
        labels_2_classification[i, :, :] = getLabel_2_classification(pilots[i])
        labels_16_classification[i * OFDMCarrierCount: OFDMCarrierCount * i + OFDMCarrierCount] = \
            getLabel_16_classification(pilots[i])
        matrixWithPilots[i * (PilotInterval + 1)] = pilots[i]
        pilotsPos[i] = i * (PilotInterval + 1)  # 记录导频在符号帧中的位置
        matrixWithPilots[(i * (PilotInterval + 1) + 1): ((i + 1) * (PilotInterval + 1))] = \
            symbolMatrix[i * PilotInterval: (i + 1) * PilotInterval]  # 1 : 4 = 1 - 3; 0 : 3 = 0 - 2
        pass

    return matrixWithPilots


#
# debug
#
if __name__ == "__main__":

    pass
