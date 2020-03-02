"""
@ OFDM仿真
@ 信号产生文件
@ DD
"""

import GlobalParameter
import numpy as np


# #
# @ func: def GetBitsNeed() -> int:
# @ 得到OFDM一个符号所拥有的比特数（信息量）
# @ para void
# @ return OFDMBitsNeed
# #
def getBitsNeed() -> int:

    ofdmBitsNeed = GlobalParameter.OFDM_Carrier_Count * GlobalParameter.Symbol_Per_Carrier \
                   * GlobalParameter.Bits_Per_Symbol

    return ofdmBitsNeed


# #
# @ func: def GetBitsNeed() -> int:
# @ 得到OFDM一个符号所拥有的比特数（信息量）
# @ para void
# @ return OFDMBitsNeed
# #
def generateBits():

    ofdmBitsNeed = getBitsNeed()  # 得到所需的比特数目
    if GlobalParameter.DEBUG:
        print(f'OFDM仿真： 单个OFDM符号所需的比特数目：{ofdmBitsNeed}')  # debug
    bits = np.random.randint(0, 2, ofdmBitsNeed)  # 得到所需的随机比特流
    if GlobalParameter.DEBUG:
        print(f'OFDM仿真： 比特流的数据类型：{type(bits)}')

    return bits


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    pass
