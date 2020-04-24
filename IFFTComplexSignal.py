"""
@ OFDM仿真
@ IFFT16QAM ofdm符号调制
@ DD
"""

import numpy as np
from numpy import floor

from BasicFunc import departComplex
from GlobalParameter import OFDMCarrierCount, IFFTLength

ofdmSymbolCarrierCount = OFDMCarrierCount


# #
# @ def ifftComplexSignal(info):
# @ 16QAM调制后IFFT
# @ para 输入复数的信息：列表
# @ return ifft后的复数符号，实部，虚部
# #
def ifftComplexSignal(info):
    # info输入时为调制完的16QAM符号流，为一个行向量
    complexArray = np.array(info).reshape(-1, ofdmSymbolCarrierCount)
    # 转为array，分组，分为符SymbolPerCarrier个OFDM符号，
    # OFDMCarrierCount个子载波叠加为一个OFDM符号。

    # carriers = np.arange(1, ofdmSymbolCarrierCount + 1) + \
    #            (floor(IFFTLength / 4) - floor(ofdmSymbolCarrierCount / 2))  # 共轭对称子载波映射 复数数据对应的IFFT点坐标
    # carriers = carriers.astype(int)  # 转换为整形内容
    # conjugate_carriers = IFFTLength - carriers + 2  # 共轭对称子载波映射,共轭复数对应的IFFT点坐标
    # conjugate_carriers = conjugate_carriers.astype(int)  # 转换为整形内容
    # IFFTModulation = np.zeros((ofdmSymbolCount, IFFTLength)).astype(complex)
    #
    # IFFTModulation[:, carriers] = complexArray  # 未添加导频信号,子载波映射在此处
    # IFFTModulation[:, conjugate_carriers] = np.conj(complexArray)  # 共轭复数映射

    # 调制每一个符号
    complexArray_IFFT = np.fft.ifft(complexArray, IFFTLength)  # 对每一行进行ifft，长度是IFFTLength，每一行得到一个调制符号
    # complexArray_IFFT_Real, complexArray_IFFT_Imag = departComplex(complexArray_IFFT)  # 分离实部和虚部

    return complexArray_IFFT


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    bits = np.random.randint(0, 2, 40)
    testArray = bits.reshape((4, 10))
    testArray_IFFT = np.fft.ifft(testArray, 16)
    testArray_IFFT2 = np.zeros_like(testArray_IFFT, complex)

    for i in np.arange(4):
        testArray_IFFT2[i] = np.fft.ifft(testArray[i], 16)
        pass

    if (testArray_IFFT == testArray_IFFT2).all():
        print("yes")

    pass
