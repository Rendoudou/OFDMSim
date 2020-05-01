"""
@ OFDM仿真
@ FFT 快速傅里叶变换
@ DD
"""

import numpy as np
from BasicFunc import departComplex
from GlobalParameter import IFFTLength, OFDMCarrierCount

FFTLength = IFFTLength


# #
# @ def fftSignalWN(signal):
# @ 对加噪后的信号FFT
# @ para signal：输入信号 array
# @ return FFT结果
# #
def fftSignalWN(signal):
    fftOutTemp = np.fft.fft(signal, FFTLength)
    fftOut = fftOutTemp[0:signal.shape[0], 0:OFDMCarrierCount]  # 得到原始数据部分，除去为快速傅里叶变化添加的0
    # realTemp, imagTemp = departComplex(fftOut)  # 分离实部和虚部

    return fftOut


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    """
    验证numpy.fft.ifft(),输入为数组时的函数执行情况
    """
    a = np.arange(9)
    b = a.reshape((3, 3))
    b_fft = np.fft.fft(b)
    b_back = np.fft.ifft(b_fft)

    c_fft = np.fft.fft(b[0, :])

    if (c_fft == b_fft[0, :]).all():
        print('yes')

    c_back = np.fft.ifft(b_fft[0, :])
    print(c_back)
    pass
