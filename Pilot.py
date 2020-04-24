"""
@ OFDM仿真
@ OFDM系统信道估计 加入导频
@ DD
@ 参考博客 https://zhuanlan.zhihu.com/p/57967971
"""

import numpy as np
from QAM16 import qam16
from GlobalParameter import OFDMCarrierCount, SymbolPerCarrier, BitsPerSymbol, PilotInterval

#
# 块状导频需要的预设导频符号流
#
def creatPilot():
    bits = np.random.randint(0, 2, OFDMCarrierCount * BitsPerSymbol)
    [agjustedSymbol, b, c, numbers] = qam16(bits)

    return np.array(agjustedSymbol)  # 返回一个已知的导频复数数组


pilots = creatPilot()  # 创建导频符号

#
# 块状导频需要的预设比特流
#
def insertPilot(qamStream):
    symbolMatrix = np.array(qamStream).reshape((-1,OFDMCarrierCount))
    pilotsNeed = int(SymbolPerCarrier / PilotInterval)
    matrixWithPilots = np.zeros((SymbolPerCarrier + pilotsNeed, OFDMCarrierCount), complex)

    for i in np.arange(pilotsNeed):  # 0 - 3
        matrixWithPilots[i * (PilotInterval + 1)] = pilots
        matrixWithPilots[(i * (PilotInterval + 1) + 1): ((i + 1) * (PilotInterval + 1))] = \
            symbolMatrix[i * PilotInterval: (i + 1) * PilotInterval]  # 1 : 4 = 1 - 3; 0 : 3 = 0 - 2
        pass

    return matrixWithPilots


#
# debug
#
if __name__ == "__main__":
    a = np.zeros((3, 4))
    print(a[0:1])
    print(a[0:2])
    print(a[0:3])

    pass
