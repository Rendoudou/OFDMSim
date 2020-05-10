"""
@ OFDM仿真
@ 瑞利分布及瑞利信道
@ DD

1.什么是瑞利分布 https://blog.csdn.net/twjy1314/article/details/62216956
瑞利分布的概率密度函数 f(x) = (x / sigma^2) * exp(-x^2 / 2 * sigma^2)  //x > 0

2.瑞利分布和瑞利信道的关系 https://blog.csdn.net/Kelvin_Yan/article/details/45404455?locationNum=4&fps=1

3.瑞利衰落，频率选择性衰落，平衰落，快衰落 http://blog.sina.com.cn/s/blog_6ce60fed01016enf.html 最好的一篇
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt, pi, cos, sin
from GlobalParameter import Fd
from NextPow2 import nextPow2


#
# 创建瑞利信道
#
def rayleigh(M, fd, t):
    """
    :param M: M为正弦波数
    :param fd: fd为最大多普勒频移
    :param t: t为时间序列
    :return: h为信道的时域表现
    """
    wd = 2 * pi * fd
    zc = np.zeros((1, len(t)))
    zs = np.zeros((1, len(t)))
    P_nor = sqrt(1 / M)
    # 引入的随机频移和变量
    alpha = np.zeros(M, float)
    for ii in np.arange(M):
        phi = 2 * pi * np.random.rand() - pi
        psi = 2 * pi * np.random.rand() - pi
        theta = 2 * pi * np.random.rand() - pi
        alpha[ii] = (2 * pi * ii - pi + theta) / 4 / M
        zc = zc + cos(cos(alpha[ii]) * wd * t + phi)
        zs = zs + cos(sin(alpha[ii]) * wd * t + psi)
        pass
    h = P_nor * (zc + 1j * zs)
    return h


#
# 画出频谱
#
def plotHW(h):
    """
    :param h: 信道时域表现
    :return: 画出频谱
    """
    h_re = h.ravel()
    # n = pow(2,nextPow2(len(h_re))+1)
    # hw = np.fft.fft(h_re,n)
    # HW = abs(hw)
    # w = np.arange(n)/n*2*pi
    plt.figure()
    plt.subplot(111)
    plt.plot(10 * np.log10(abs(h_re)))
    plt.axis([0, 5000, -7, 10])
    plt.xlabel('w')
    plt.ylabel('Hw/dB')
    plt.show()
    pass

#
# debug
#
if __name__ == "__main__":
    # t = np.arange(0, 5, 0.00001)
    # chan = rayleigh(120, 100, t)
    # plotHW(chan)
    pass
