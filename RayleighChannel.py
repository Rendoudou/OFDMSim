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
from numpy import sqrt, pi, cos


def rayleigh(fd, t):
    """
    # %改进的jakes模型来产生单径的平坦型瑞利衰落信道
    # %Yahong R.Zheng and Chengshan Xiao "Improved Models for
    # %the Generation of Multiple Uncorrelated Rayleigh Fading Waveforms"
    # %IEEE Commu letters, Vol.6, NO.6, JUNE 2002
    # %输入变量说明：
    # %  fd：信道的最大多普勒频移 单位Hz
    # %  t :信号的抽样时间序列，抽样间隔单位s
    # %  h为输出的瑞利信道函数，是一个时间函数复序列
    """
    # 假设的入射波数目
    N = 40
    wm = 2 * pi * fd
    # 每象限的入射波数目即振荡器数目
    N0 = N / 4
    # 信道函数的实部
    Tc = np.zeros((1, len(t)))
    # 信道函数的虚部
    Ts = np.zeros((1, len(t)))
    # 归一化功率系数
    P_nor = sqrt(1 / N0)
    # 区别个条路径的均匀分布随机相位

    alfa = np.zeros((1, N0), float)
    for ii in np.arange(N0):  # 1:N0
        # 对每个子载波而言在(-pi,pi)之间均匀分布的随机相位
        fi_tc = 2 * pi * np.random.rand(1, 1) - pi
        fi_ts = 2 * pi * np.random.rand(1, 1) - pi
        # 第i条入射波的入射角
        theta = 2 * pi * np.random.rand(1, 1) - pi
        alfa[ii] = (2 * pi * ii - pi + theta) / N
        # 计算冲激响应函数
        Tc = Tc + cos(np.cos(alfa[ii]) * wm * t + fi_tc)
        Ts = Ts + cos(np.sin(alfa[ii]) * wm * t + fi_ts)
        pass
    # 乘归一化功率系数得到传输函数
    h = P_nor * (Tc + 1j * Ts)

    return h


if __name__ == "__main__":
    t = np.arange(0,1,0.0001)
    chan = rayleigh(100, t)

    pass