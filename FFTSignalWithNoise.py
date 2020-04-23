"""
@ OFDM仿真
@ FFT 快速傅里叶变换
@ DD
"""

import numpy as np
from BasicFunc import departComplex
from GlobalParameter import IFFTLength, OFDMCarrierCount, SymbolPerCarrier

FFTLength = IFFTLength


# #
# @ def fftSignalWN(signal):
# @ 对加噪后的信号FFT
# @ para signal：输入信号 array
# @ return FFT结果
# #
def fftSignalWN(signal):
    fftOutTemp = np.fft.fft(signal, FFTLength)
    fftOut = fftOutTemp[0:SymbolPerCarrier, 0:OFDMCarrierCount]  # 得到原始数据部分，除去为快速傅里叶变化添加的0
    # realTemp = np.zeros(signal.shape[0])
    # imagTemp = np.zeros(signal.shape[0])
    #
    # for i in range(fftOut.shape[0]):
    #     realTemp[i] = fftOut[i].real
    #     imagTemp[i] = fftOut[i].imag

    realTemp, imagTemp = departComplex(fftOut)

    return fftOut, realTemp, imagTemp


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

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
