"""
@ OFDM仿真
@ 信道中，信号与信道特征卷积
@ DD
"""
import numpy as np

from ChannelConv import ConvLength
from ChannelConv import LenH
from Pilot import pilotsPos


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
    h_get_fft = np.zeros((len(pilotsPos), ConvLength), complex)

    h_out = np.zeros(LenH, complex)
    h_out_fft = np.zeros(ConvLength, complex)

    for i in np.arange(len(pilotsPos)):
        signal_degra = list(pilots_cp_ch_awgn[i])  # 长度相比较长
        signal = list(pilots_cp[i])  # 经过信道
        for j in np.arange(len(signal_degra) - len(signal)):  # 转换为圆周卷积长度
            signal.append(complex(0))
            pass
        a_fft = np.fft.fft(signal_degra)  # 输出长度默认为为输入的数据长度
        b_fft = np.fft.fft(signal)

        h_get_fft[i] = a_fft / b_fft  # 获得信道频谱
        h_temp = np.fft.ifft(h_get_fft[i])
        h_get[i] = h_temp[0: LenH: 1]  # 获得信道时域

        h_out_fft = h_out_fft + h_get_fft[i]
        h_out = h_out + h_get[i]
        pass

    h_out = h_out / len(pilotsPos)
    h_out_fft = h_out_fft / len(pilotsPos)
    return h_out, h_out_fft

#
# 削弱信道影响
#
def weakenChannelInterf(ofdm_cp_ch_awgn, ofdm_cp):
    """
    :param ofdm_cp_ch_awgn: 经过信道和加噪声的ofdm符号
    :param ofdm_cp: 进入信道前的ofdm符号
    :return: 简易信道估计后,输出矫正结果
    """
    h_est, h_est_fft = estimateChannelH(ofdm_cp_ch_awgn, ofdm_cp)

    temp_fft = np.zeros_like(ofdm_cp_ch_awgn, complex)
    temp_fft_rectify = np.zeros_like(ofdm_cp_ch_awgn, complex)
    temp_rectify = np.zeros_like(ofdm_cp, complex)

    for i in np.arange(ofdm_cp_ch_awgn.shape[0]):
        temp_fft[i] = np.fft.fft(ofdm_cp_ch_awgn[i])  # 卷积后长度
        temp_fft_rectify[i] = temp_fft[i] / h_est_fft  # 解除卷积
        temp_rectify[i] = np.fft.ifft(temp_fft_rectify[i])[0: ofdm_cp.shape[1]: 1]  # 矫正结果
        pass
    return temp_rectify


#
# debug
#
if __name__ == "__main__":
    b = np.array([0, 1, 3])
    test = np.zeros((4, 4), int)
    a = test[b]
    pass
