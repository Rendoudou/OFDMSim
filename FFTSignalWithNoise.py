"""
@ OFDM仿真
@ FFT 快速傅里叶变换
@ DD
"""

import numpy as np
from BasicFunc import departComplex
from GlobalParameter import IFFTLength
FFTLength = IFFTLength

# #
# @ def fftSignalWN(signal):
# @ 对加噪后的信号FFT
# @ para signal：输入信号 array
# @ return FFT结果
# #
def fftSignalWN(signal):

    fftOut = np.fft.fft(signal,FFTLength)

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

    pass