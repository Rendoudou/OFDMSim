"""
@ OFDM仿真
@ IFFT16QAM
@ DD
"""

import numpy as np
from numpy import floor

from BasicFunc import departComplex
from GlobalParameter import OFDMCarrierCount, SymbolPerCarrier, IFFTLength


# #
# @ def ifftComplexSignal(info):
# @ 16QAM调制后IFFT
# @ para 输入复数的信息：列表
# @ return ifft后的复数符号，实部，虚部
# #
def ifftComplexSignal(info):
    # info输入时为调制完的16QAM符号流，为一个行向量
    complexArray = np.array(info).reshape(SymbolPerCarrier, OFDMCarrierCount)  # 转为array，分组，分为多个符号，多个子载波叠加。

    carriers = np.arange(1, OFDMCarrierCount + 1) + \
               (floor(IFFTLength / 4) - floor(OFDMCarrierCount / 2))  # 共轭对称子载波映射 复数数据对应的IFFT点坐标
    carriers = carriers.astype(int)  # 转换为整形内容
    conjugate_carriers = IFFTLength - carriers + 2  # 共轭对称子载波映射,共轭复数对应的IFFT点坐标
    conjugate_carriers = conjugate_carriers.astype(int)  # 转换为整形内容
    IFFTModulation = np.zeros((SymbolPerCarrier, IFFTLength)).astype(complex)
    IFFTModulation[:, carriers] = complexArray  # 未添加导频信号,子载波映射在此处
    IFFTModulation[:, conjugate_carriers] = np.conj(complexArray)  # 共轭复数映射

    complexArray_IFFT = np.fft.ifft(complexArray, IFFTLength)

    complexArray_IFFT_Real, complexArray_IFFT_Imag = departComplex(complexArray_IFFT)

    return complexArray_IFFT, complexArray_IFFT_Real, complexArray_IFFT_Imag


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    pass
