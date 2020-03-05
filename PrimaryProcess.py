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

from BasicFunc import plotSignalScatter,getComplexSignalPower
from GenerteSignal import generateBits
from QAM16 import qam16
from IFFTComplexSignal import ifftComplexSignal
from AddWGN import addAWGNComplex
#from GlobalParameter import SNR
from FFTSignalWithNoise import fftSignalWN
from DecodeQAM16 import DecodeQAM16
from Anlysis import calcMismatchRatio
from GlobalParameter import PrimaryProcessDebug


# #
# @ Debug
# #
def primaryProcess(snr):
    """
    随机产生原始比特流
    """
    originalBits = generateBits()

    """
    经过16QAM调制
    """
    complexStreamQAM, complexStreamQAM_Real, complexStreamQAM_Imag, numberOrigin = \
        qam16(originalBits)
    if PrimaryProcessDebug:
        plotSignalScatter(complexStreamQAM_Real, complexStreamQAM_Imag, len(complexStreamQAM), 1)

    """
    IFFT 快速傅里叶逆变换
    """
    complexStreamIFFT, complexStreamIFFT_Real, complexStreamIFFT_Imag = \
        ifftComplexSignal(complexStreamQAM)

    """
    IFFT后 信号加噪声 进入高斯信道。此处是分为两路，再分开加噪声。合理吗？ 
    """
    FFTInputArray, FFTInputArray_Real, FFTInputArray_Imag = \
        addAWGNComplex(complexStreamIFFT_Real, complexStreamIFFT_Imag, snr)

    if PrimaryProcessDebug:
        Ps = getComplexSignalPower(complexStreamIFFT)
        Pn = getComplexSignalPower(FFTInputArray - complexStreamIFFT)
        snr_out = 10 * np.log10(Ps / Pn)

    """
    FFT 快速傅里叶变换
    """
    FFTOutputArray, FFTOutputArray_Real, FFTOutputArray_Imag = fftSignalWN(FFTInputArray)
    if PrimaryProcessDebug:
        plotSignalScatter(FFTOutputArray_Real, FFTOutputArray_Imag, FFTOutputArray.shape[0], 2)  # 接收后FFT画图，加噪声后 16QAM

    """
    解调
    """
    outBits, outNumber = DecodeQAM16(FFTOutputArray_Real, FFTOutputArray_Imag)

    """
    误比特率或者误码率
    """
    errorRatio = calcMismatchRatio(originalBits, np.array(outBits))

    """
    计算和显示重要信息,when debug
    """
    if PrimaryProcessDebug:
        snrPr = format(snr, '.3f')
        snr_outPr = format(snr_out, '.3f')
        correctRatioPr = format(100 - errorRatio * 100, '.4f')
        print(f'SNR in {snrPr}dB, real in {snr_outPr}dB. correct Ratio : {correctRatioPr} %')
        plt.show()

    return errorRatio


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    primaryProcess(0)

    pass