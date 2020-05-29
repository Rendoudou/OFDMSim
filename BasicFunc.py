"""
@ OFDM仿真
@ 基础函数 输入输出 画图 清屏
@ DD
"""

import numpy as np
from matplotlib import pylab as plt
from GlobalParameter import TxLength

x1 = np.arange(-5, 5, 0.1)
x2 = np.zeros_like(x1)

y2 = np.arange(-5, 5, 0.1)
y1 = np.zeros_like(y2)

# #
# @ def ifftComplexSignal(info):
# @ 16QAM调制后IFFT
# @ para 输入复数的信息：列表
# @ return ifft后的复数符号，实部，虚部
# #
def plotSignalScatter(symbol):
    symbolIn = np.array(symbol)
    symbol_r = symbolIn.real
    symbol_i = symbolIn.imag

    plt.figure()
    plt.scatter(symbol_r, symbol_i)  # 实部 虚部 画星座图 a array 从0到n-1
    plt.plot(x1, x2, color='red')
    plt.plot(y1, y2, color='red')
    plt.xlabel('real')
    plt.ylabel('imag')
    plt.grid(True)
    plt.show()
    pass


# #
# @ def toComplex(real, imag):
# @ 将分开的实部和虚部转换为复数信号
# @ para real实部，imag 虚部
# @ return void
# #
def toComplex(real, imag):
    if real.shape != imag.shape:
        print("OFDM仿真：error func toComplex() ")

    tempArray = real + imag * 1j

    return tempArray  # 转换为numpy.array 返回


# #
# @ def departComplex(array):
# @ 分离一个复数数组的实部和虚部
# @ para array 需要分离的数组
# @ return void
# #
def departComplex(array):
    realTemp = np.real(array)
    imagTemp = np.imag(array)

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

    s_temp[0] = s_temp_real
    s_temp[1] = s_temp_imag

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
# @ def beLine(signal):
# @ 串并转换
# @ para signal
# @ return 变换后信号
# #
def beLine(signal):
    return signal.reshape((1,-1))


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    pass
