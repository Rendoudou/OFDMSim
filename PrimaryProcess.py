"""
@ OFDM仿真，加入线性回归，学习X&Y轴，修正接收信号。
@ 主函数文件
@ DD
"""
import numpy as np

from BasicFunc import plotSignalScatter, getComplexSignalPower # 画出星座图，获得信号功率

from GenerateBits import generateBits               # 产生源数据
from QAM16 import qam16                             # 16QAM调制
from Pilot import insertPilot                       # 插入导频
from IFFTComplexSignal import ifftComplexSignal     # 调制为ofdm符号
from AddDeleteCP import addCP                       # 加入循环前缀
                                                    # 并串转换
from ChannelConv import ofdmConvChannelH            # 2-tap channel
from AddWGN import AWGNComplex2                     # 加入高斯噪声
from ChannelConv import ConvLength                  # 串并转换,经过信道后，符号长度变化
from ChannelEstimationH import weakenChannelInterf  # 简易信道估计，去部分信道影响
from FFTSignalWithNoise import fftSignalWN          # 解调ofdm信号
from AddDeleteCP import deleteCP                    # 去循环前缀
from MachineLearning import trainAxis               # 机器学习，线性回归计算畸变横纵坐标
from Rectify import rectify                         # 矫正坐标
from DecodeQAM16 import DecodeQAM16                 # 解码16QAM
from Anlysis import calcMismatchRatio               # 计算误码率


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
    qam, numberOrigin = qam16(originalBits)
    if PrimaryProcessDebug:
        plotSignalScatter(qam, 1)

    """
        插入导频,另一组信号插入了导频
    """
    qam_p = insertPilot(qam)

    """
    IFFT 快速傅里叶逆变换，实现多载波信号快速调制产生结果
    """
    ofdmSignal_p = ifftComplexSignal(qam_p)

    """
    加循环前缀,和循环后缀
    """
    ofdm_p_cp = addCP(ofdmSignal_p)

    """
    并串转换,信道传输
    """
    info_pTx = ofdm_p_cp.ravel()  # TxLength = symbolPerCarrier * (carriers + GI + GIP)

    """
    经过 2-tap 信道
    """
    info_pTx_ch = ofdmConvChannelH(info_pTx)

    """
    信号经过信道，加噪声。此处是分为两路，再分开加噪声。 
    """
    # info_pRx_ch = AWGNComplex2(info_pTx_ch, snr)
    info_pRx_ch = info_pTx_ch
    if PrimaryProcessDebug:
        Ps = getComplexSignalPower(info_pTx_ch)
        Pn = getComplexSignalPower(info_pRx_ch - info_pTx_ch)
        snrOut = 10 * np.log10(Ps / Pn)

    """
    串并转换
    """
    ofdm_p_cp_ch_awgn = info_pRx_ch.reshape((-1, ConvLength))  # 卷积后的长度

    """
    简易信道估计,消除信道影响
    """
    ofdm_p_cp_awgn = weakenChannelInterf(ofdm_p_cp_ch_awgn, ofdm_p_cp)

    """
    去循环前缀和循环后缀
    """
    ofdm_p_awgn = deleteCP(ofdm_p_cp_awgn)

    """
    FFT 快速傅里叶变换
    """
    qam_p_awgn = fftSignalWN(ofdm_p_awgn)
    if PrimaryProcessDebug:
        plotSignalScatter(qam_p_awgn, 2)  # 接收后FFT画图，加噪声后 16QAM

    """
        基于导频训练分界线
    """
    weights_x, weights_y = trainAxis(qam_p_awgn)  # 整体坐标系产生的偏移

    """
        基于分界线做出修正
    """
    qam_p_awgn_rec = rectify(qam_p_awgn, weights_x, weights_y)

    """
    解调
    """
    outBits, outNumber = DecodeQAM16(qam_p_awgn)  # 解码,输出部分去掉了导频。具体实现见函数
    outBits_rec, outNumber_rec = DecodeQAM16(qam_p_awgn_rec)  # 解码,输出部分去掉了导频。具体实现见函数

    """
    误比特率或者误码率
    """
    [errorRatio, errorCount] = calcMismatchRatio(originalBits, outBits)
    [errorRatio_rec, errorCount_rec] = calcMismatchRatio(originalBits, outBits_rec)

    """
    计算和显示重要信息,when debug
    """
    if PrimaryProcessDebug:
        snrPr = format(snr, '.3f')
        snr_outPr = format(snrOut, '.3f')
        correctRatioPr = format(100 - errorRatio * 100, '.4f')
        correctRatioPr_rec = format(100 - errorRatio_rec * 100, '.4f')
        print(f'SNR in {snrPr}dB, real in {snr_outPr}dB. correct Ratio : {correctRatioPr} %. '
              f'rec correct Ratio : {correctRatioPr_rec} %.')
        # plt.show()
        pass

    return errorCount, errorCount_rec


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    PrimaryProcessDebug = True
    primaryProcess(5)
    pass
