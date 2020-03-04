"""
@ OFDM仿真
@ QAM16调制
@ DD
"""

import numpy as np
from GlobalParameter import Bits_Per_Symbol  # 每个符号所带的比特数目
from BasicFunc import departComplex
from GlobalParameter import mapping


# #
# @ func: def translateBits(bits: list) -> int:
# @ 二进制转10进制
# @ para 输入比特流
# @ return 10进制
# #
def translateBits(bits) -> int:
    if len(bits) != Bits_Per_Symbol:
        print("OFDM仿真：error，translateBits")
        SystemExit()
        pass
    temp = bits[0] * 1 + bits[1] * 2 + bits[2] * 4 + bits[3] * 8

    return temp


# #
# @ func: def QAM16(bits: list) -> list:
# @ 16QAM调制
# @ para 输入比特流
# @ return 复数符号，实部，虚部
# #
def qam16(bits: list):
    complexList = []  # list void
    bitsReshape = np.reshape(bits, (int(len(bits) / 4), 4))  # 比特流列表重构，变为n/4行，4列。array 相当与串并转换
    numberList = []

    for i in range(bitsReshape.shape[0]):  # shape[0] 行数
        temp = translateBits(bitsReshape[i, :])  # 转为十进制
        keyTemp = str(temp)
        numberList.append(temp)
        complexList.append(complex(mapping[keyTemp][0], mapping[keyTemp][1]))  # list
        pass

    # complexListReal_array = np.zeros(bitsReshape.shape[0])  # array 存储16QAM调制后的实部
    # complexListImg_array = np.zeros(bitsReshape.shape[0])  # array 存储16QAM调制后的虚部
    #
    # for i in range(bitsReshape.shape[0]):
    #     complexListReal_array[i] = complexList[i].real
    #     complexListImg_array[i] = complexList[i].imag

    complexListReal_array, complexListImg_array = departComplex(np.array(complexList))  # 分离实部和虚部

    return complexList, complexListReal_array, complexListImg_array, numberList


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    pass
