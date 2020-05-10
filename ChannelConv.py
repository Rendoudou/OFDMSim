"""
@ OFDM仿真
@ 信道中，信号与信道特征卷积
@ DD
"""
import numpy as np
from GlobalParameter import SymbolLength  # 调制后发入信道的ofdm符号长度

#
# two-tap channel
#
def getTwoTapChannel():
    """
    :param: void
    :return: generates a (2-tap) channel
    """
    h =np.array([np.random.rand() + 1j * np.random.rand() , (np.random.rand() + 1j * np.random.rand()) / 2])
    return h

h = getTwoTapChannel()
ConvLength = SymbolLength + len(h) - 1
LenH = 2

#
# 信号卷积,输入的信号是经过ifft变换，串并转换的发射信号
#
def ofdmConvChannelH(ofdmStream):
    """
    :param ofdmStream: 一帧ofdm符号,长度为n * SymbolLength
    :return: 卷积后结果
    """
    symbol_reshape = ofdmStream.reshape((-1, SymbolLength))
    n = symbol_reshape.shape[0]
    symbol_out = np.zeros((n, ConvLength), complex)
    if n > 0:
        for i in np.arange(n):
            symbol_out[i] = np.convolve(symbol_reshape[i], h, mode='full')  # 正常卷积
            pass
        pass
    else:
        print("error, ofdmConvChannelH()")
        pass
    return symbol_out.ravel() # 拉直，假设发射时不同符号之间时间间隔足够,变回发射在空中的状态。

#
# debug
#
if "__main__" == __name__:

    pass

