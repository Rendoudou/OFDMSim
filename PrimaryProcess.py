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
#from GlobalParameter import SNR
from FFTSignalWithNoise import fftSignalWN
from DecodeQAM16 import DecodeQAM16
from Anlysis import calcMismatchRatio
from GlobalParameter import PrimaryProcessDebug


# #
# @ Debug
# #
def PrimaryProcess(snr):
    """
    随机产生原始比特流
    """
    originalBits = generateBits()

    """
    经过16QAM调制
    """
    complexStreamQAM, complexStreamQAM_Real, complexStreamQAM_Imag = \
        qam16(originalBits)
    if PrimaryProcessDebug:
        plotSignalScatter(complexStreamQAM_Real, complexStreamQAM_Imag, len(complexStreamQAM), 1)

    """
    IFFT 快速傅里叶逆变换
    """
    complexStreamIFFT, complexStreamIFFT_Real, complexStreamIFFT_Imag = \
        ifftComplexSignal(complexStreamQAM)

    # plt.figure(1,figsize=(10, 16))
    # plt.subplot(211)
    # plt.psd(complexStreamIFFT)
    # plt.title("original signal after IFFT")

    """
    IFFT后 信号加噪声 进入高高斯信道
    """
    FFTInputArray, FFTInputArray_Real, FFTInputArray_Imag = \
        addAWGNComplex(complexStreamIFFT_Real, complexStreamIFFT_Imag, snr)

    """
    FFT 快速傅里叶变换
    """
    FFTOutputArray, FFTOutputArray_I, FFTOutputArray_Q = fftSignalWN(FFTInputArray)
    if PrimaryProcessDebug:
        plotSignalScatter(FFTOutputArray_I, FFTOutputArray_Q, FFTOutputArray.shape[0], 2)  # 接收后FFT画图，加噪声后 16QAM

    # plt.subplot(212)
    # plt.psd(FFTOutputArray)
    # plt.title("add wgn")

    """
    解调
    """
    outBits = DecodeQAM16(FFTOutputArray_I, FFTOutputArray_Q)

    """
    误比特率或者误码率
    """
    errorRatio = calcMismatchRatio(originalBits, np.array(outBits))

    """
    计算和显示重要信息
    """
    snrPr = format(snr,'.3f')
    correctRatioPr = format(100 - errorRatio * 100,'.4f')
    print(f'SNR in {snrPr}dB, correct Ratio : {correctRatioPr} %')

    if PrimaryProcessDebug:
        plt.show()
    plt.show()

    return 100 - errorRatio * 100


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    PrimaryProcess(5)

    pass