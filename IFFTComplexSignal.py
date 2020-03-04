"""
@ OFDM仿真
@ IFFT16QAM
@ DD
"""

import numpy as np
from BasicFunc import departComplex


# #
# @ def ifftComplexSignal(info):
# @ 16QAM调制后IFFT
# @ para 输入复数的信息：列表
# @ return ifft后的复数符号，实部，虚部
# #
def ifftComplexSignal(info):

    complexArray = np.array(info)  # 转为array
    complexArray_IFFT = np.fft.ifft(complexArray)

    complexArray_IFFT_Real, complexArray_IFFT_Imag = departComplex(complexArray_IFFT)

    return complexArray_IFFT, complexArray_IFFT_Real, complexArray_IFFT_Imag


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    pass
