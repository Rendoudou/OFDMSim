"""
@ OFDM仿真
@ 信道中，信号与信道特征卷积
@ DD
"""
import numpy as np
import scipy.signal as ss
from Pilot import pilotsPos
from ChannelConv import LenH


#
# 简单信道估计
#
def estimateChannelH(ofdm_cp_ch_awgn, ofdm_cp):
    """
    :param ofdm_cp_ch_awgn: 经过信道和加噪声的ofdm符号
    :param ofdm_cp: 进入信道前的ofdm符号
    :return: 简易信道估计结果
    """
    pilots_cp = ofdm_cp[pilotsPos]
    pilots_cp_ch_awgn = ofdm_cp_ch_awgn[pilotsPos]
    h_get = np.zeros((len(pilotsPos), LenH), complex)
    h_out = np.zeros(LenH, complex)
    for i in np.arange(len(pilotsPos)):
        a = list(pilots_cp_ch_awgn[i])
        b = list([pilots_cp[i], 0])
        a_fft = np.fft.fft(a)
        b_fft = np.fft.fft(b)
        h_fft = a_fft / b_fft
        h_get[i] = (np.fft.ifft(h_fft))[0: 1]
        h_out = h_out + h_get[i]
        pass

    h_out = h_out / len(pilotsPos)
    return h_out


#
# 削弱信道影响
#
def weakenChannelInterf(ofdm_cp_ch_awgn, ofdm_cp):
    """
    :param ofdm_cp_ch_awgn: 经过信道和加噪声的ofdm符号
    :param ofdm_cp: 进入信道前的ofdm符号
    :return: 简易信道估计结果
    """
    ofdm_cp_awgn = np.zeros_like(ofdm_cp,complex)
    h = estimateChannelH(ofdm_cp_ch_awgn, ofdm_cp)

    return ofdm_cp_awgn


#
# debug
#
if __name__ == "__main__":
    b = np.array([0, 1, 3])
    test = np.zeros((4, 4), int)
    a = test[b]
    pass
