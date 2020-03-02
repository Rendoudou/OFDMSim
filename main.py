"""
@ OFDM仿真，未加入机器学习
@ 主函数文件
@ DD
"""

import matplotlib.pyplot as plt
import numpy as np

# import GenerateSignal
# import QAM16
# import IFFTComplexSignal
# import BasicFunc

from BasicFunc import plotSignalScatter
from GenerteSignal import generateBits
from QAM16 import qam16
from IFFTComplexSignal import ifftComplexSignal
from AddAWGN import addAWGNComplex
from GlobalParameter import SNR
from FFTSignalWithNoise import fftSignalWN

# #
# @ Debug
# #
if __name__ == "__main__":
    """
    随机产生原始比特流
    """
    originalBits = generateBits()

    """
    经过16QAM调制
    """
    complexStreamQAM, complexStreamQAM_Real, complexStreamQAM_Imag = \
        qam16(originalBits)
    plotSignalScatter(complexStreamQAM_Real, complexStreamQAM_Imag, len(complexStreamQAM),1)

    # print(f'QAM16: \n {complexStreamQAM}')
    # print(len(complexStreamQAM))
    #
    # print(np.array(complexStreamQAM))
    # print(np.array(complexStreamQAM).shape)

    """
    IFFT 快速傅里叶逆变换
    """
    complexStreamIFFT, complexStreamIFFT_Real, complexStreamIFFT_Imag = \
        ifftComplexSignal(complexStreamQAM)
    # plt.figure(figsize=(20, 32))
    # plt.subplot(111)
    # plt.psd(complexStreamIFFT)
    # plt.grid(True)
    # plt.show()

    """
    IFFT后 信号加噪声 进入高高斯信道
    """
    FFTInputArray, FFTInputArray_Real, FFTInputArray_Imag = \
        addAWGNComplex(complexStreamIFFT_Real, complexStreamIFFT_Imag, SNR)
    plotSignalScatter(FFTInputArray_Real, FFTInputArray_Imag, FFTInputArray.shape[0],2)

    """
    FFT 快速傅里叶变换
    """
    FFTOutputArray, FFTOutputArray_Real,  FFTOutputArray_Imag= fftSignalWN(FFTInputArray)
    plotSignalScatter(FFTOutputArray_Real, FFTOutputArray_Imag, FFTOutputArray.shape[0], 3)

    plt.show()

    pass
