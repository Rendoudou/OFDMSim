"""
@ OFDM仿真，未完全加入机器学习
@ 主函数文件
@ DD
"""

import matplotlib.pyplot as plt
import numpy as np

# import GenerateSignal
# import QAM16
# import IFFTComplexSignal
# import BasicFunc

from GlobalParameter import SymbolPerCarrier, TxLength
from BasicFunc import plotSignalScatter, getComplexSignalPower
from GenerateSignal import generateBits
from QAM16 import qam16
from IFFTComplexSignal import ifftComplexSignal
from AddWGN import AWGNComplex2
# from GlobalParameter import SNR
from FFTSignalWithNoise import fftSignalWN
from DecodeQAM16 import DecodeQAM16
from Anlysis import calcMismatchRatio
from AddDeleteCP import addCP, deleteCP
# 文件内调试用参数
PrimaryProcessDebug = False
snrOut = 0.0


# #
# @ Debug
# #
def primaryProcess(snr):
    """
    :param snr: 输入信噪比
    :return: 误码率
    """

    global snrOut

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
        plotSignalScatter(complexStreamQAM_Real, complexStreamQAM_Imag, 1)

    """
    IFFT 快速傅里叶逆变换，实现多载波信号快速调制产生结果
    """
    complexArrayIFFT, complexArrayIFFT_Real, complexArrayIFFT_Imag = \
        ifftComplexSignal(complexStreamQAM)

    """
    加循环前缀,和循环后缀
    """
    complexArrayWithCP = addCP(complexArrayIFFT)  # 加入循环前缀和循环后缀 数据规模（symbolPerCarrier * (carriers + GI + GIP)）

    """
    并串转换
    """
    infoTx = complexArrayWithCP.ravel()  # TxLength = symbolPerCarrier * (carriers + GI + GIP)

    """
    信号加噪声后  进入高斯信道。此处是分为两路，再分开加噪声。合理吗？ 
    """
    infoRx = AWGNComplex2(infoTx, snr)
    if PrimaryProcessDebug:
        Ps = getComplexSignalPower(infoTx)
        Pn = getComplexSignalPower(infoRx - infoTx)
        snrOut = 10 * np.log10(Ps / Pn)

    """
    串并转换
    """
    complexArrayRx = infoRx.reshape((SymbolPerCarrier, int(TxLength / SymbolPerCarrier)))  # 转换为更易理解的矩阵

    """
    去循环前缀和循环后缀
    """
    complexArrayUsePart = deleteCP(complexArrayRx)  # 去多余

    """
    FFT 快速傅里叶变换
    """
    complexArrayFFTOut, complexArrayFFTOut_Real, complexArrayFFTOut_Imag = fftSignalWN(complexArrayUsePart)
    if PrimaryProcessDebug:
        plotSignalScatter(complexArrayFFTOut_Real, complexArrayFFTOut_Imag, 2)  # 接收后FFT画图，加噪声后 16QAM

    """
    解调
    """
    outBits, outNumber = DecodeQAM16(complexArrayFFTOut_Real, complexArrayFFTOut_Imag)

    """
    误比特率或者误码率
    """
    errorRatio = calcMismatchRatio(originalBits, np.array(outBits))

    """
    计算和显示重要信息,when debug
    """
    if PrimaryProcessDebug:
        snrPr = format(snr, '.3f')
        snr_outPr = format(snrOut, '.3f')
        correctRatioPr = format(100 - errorRatio * 100, '.4f')
        print(f'SNR in {snrPr}dB, real in {snr_outPr}dB. correct Ratio : {correctRatioPr} %')
        plt.show()

    return errorRatio


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    PrimaryProcessDebug = True
    primaryProcess(10)

    pass
