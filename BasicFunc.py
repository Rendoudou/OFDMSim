"""
@ OFDM仿真
@ 基础函数 输入输出 画图 清屏
@ DD
"""

import numpy as np
from matplotlib import pylab as plt


# #
# @ def ifftComplexSignal(info):
# @ 16QAM调制后IFFT
# @ para 输入复数的信息：列表
# @ return ifft后的复数符号，实部，虚部
# #
def plotSignalScatter(a, b, n: int, pos):
    plt.figure(int(pos))
    plt.scatter(a[0:int(n)], b[0:int(n)])  # 实部 虚部 画星座图 a array 从0到n-1
    plt.title(f'plot img {pos}')

    pass


# #
# @ def toComplex(real, imag):
# @ 将分开的实部和虚部转换为复数信号
# @ para real实部，imag 虚部
# @ return void
# #
def toComplex(real, imag):
    if real.shape[0] != imag.shape[0]:
        print("OFDM仿真：error func toComplex() ")

    temp = []
    for i in range(real.shape[0]):
        temp.append(real[i] + imag[i] * 1j)

    return np.array(temp)  # 转换为numpy.array 返回


# #
# @ def departComplex(array):
# @ 分离一个复数数组的实部和虚部
# @ para array 需要分离的数组
# @ return void
# #
def departComplex(array):
    realTemp = np.zeros(array.shape[0])
    imagTemp = np.zeros(array.shape[0])

    for i in range(array.shape[0]):
        realTemp[i] = array[i].real
        imagTemp[i] = array[i].imag

    return realTemp, imagTemp


# #
# @ def getComplexSignalPower(signal):
# @ 复数信号的功率
# @ para array 复数信号
# @ return void
# #
def getComplexSignalPower(signal):
    s_temp = np.zeros((2, len(signal)))
    s_temp_real, s_temp_imag = departComplex(signal)

    s_temp[0, ] = s_temp_real
    s_temp[1, ] = s_temp_imag

    power = np.linalg.norm(s_temp) ** 2 / s_temp.size

    return power


# #
# @ def process_bar(percent, start_str='', end_str='', total_length=0):
# @ 进度条
# @ para percent
# @ return void
# #
def processBar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m" % '   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    pass
