"""
@ OFDM仿真
@ 高斯信道 噪声
@ DD
"""

import matplotlib.pylab as plt
import numpy as np

from BasicFunc import toComplex


# #
# @ func: def QAM16(bits: list) -> list:
# @ 高斯白噪声
# @ para x 输入信号，信噪比
# @ return 加性噪声
# #
def wgn(x, snr):
    snrTemp = 10 ** (snr / 10.0)
    xpower = np.sum(abs(x) ** 2) / len(x)  # 输入信号的功率
    npower = xpower / snrTemp  # 噪声应有的功率

    return np.random.randn(len(x)) * np.sqrt(npower)
    # P_signal = np.sum(abs(x) ** 2) / len(x)  # 原始信号功率
    # P_noise = P_signal / (10 ** (snr / 10.0))
    # return np.random.randn(len(x)) * np.sqrt(P_noise)


# #
# @ func: def awgn(real, imag, snr):
# @ 信号加噪声
# @ para real 输入信号实部， imag 输入信号虚部， snr 信噪比
# @ return 加噪结果
# #
def awgn(real, imag, snr):
    realTemp = real + wgn(real, snr)
    imagTemp = imag + wgn(imag, snr)

    complexSignalAddAwgn = toComplex(realTemp, imagTemp)

    return complexSignalAddAwgn, realTemp, imagTemp


# #
# @ func: def addAWGNComplex(real, imag, snr):
# @ 信号加噪声
# @ para real 输入信号实部, imag 输入信号虚部， snr 信噪比
# @ return 加噪结果
# #
def addAWGNComplex(real, imag, snr):

    length = real.shape[0]
    signal = np.zeros((2,length))
    signal[0,] = real
    signal[1,] = imag

    noise = np.random.randn(signal.shape[0], signal.shape[1])  # 产生N(0,1)噪声数据
    noise = noise - np.mean(noise)  # 均值为0
    signal_power = np.linalg.norm(signal) ** 2 / signal.size  # 此处是信号的std**2
    noise_variance = signal_power / np.power(10, (snr / 10))  # 此处是噪声的std**2
    noise = (np.sqrt(noise_variance) / np.std(noise)) * noise  # 此处是噪声的std**2

    noise_power = np.linalg.norm(noise) ** 2 / noise.size

    # print(signal_power)
    # print(noise_power)
    # print(f'snr : {10 * np.log10(signal_power / noise_power)} dB')

    signal_noise = noise + signal
    signal_complex = toComplex(signal_noise[0,], signal_noise[1,])
    real_noise = signal_noise[0,]
    imag_noise = signal_noise[1,]

    return signal_complex, real_noise, imag_noise


# #
# @ func: def addAWGN(x, snr):
# @ 信号加噪声
# @ para x 信号 snr 信噪比
# @ return 加噪结果
# #
def addAWGN(x, snr):
    return x + wgn(x, snr)


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    a = np.array([1, -1, 3, 3])
    b = np.array([3, 3, -3, 3])
    s_noise_C, s_noise_real, s_noise_imag = addAWGNComplex(a, b, 0.1)


    # 测试噪声
    t = np.arange(0, 100000) * 0.01
    a = np.cos(t)

    plt.figure(figsize=(20, 32))

    plt.subplot(221)  # 两行两列第一个位置
    plt.plot(t, a)
    plt.title("before add awgn")

    # b =  a + wgn(a, 6)
    b = addAWGN(a, 1)
    plt.subplot(222)  # 两行两列第二个位置
    plt.plot(t, b)
    plt.title("after add awgn")

    plt.subplot(223)  # 两行两列第三个位置
    n = wgn(a, 0.1)
    plt.hist(n, bins=100, density=True)

    plt.subplot(224)  # 两行两列第四个位置
    plt.psd(n)

    plt.show()

    # plt.figure(1, figsize=(10, 12))
    # plt.subplot(221)
    # plt.psd(real)
    # plt.title("signal")
    #
    # plt.subplot(222)
    # plt.psd(realTemp)
    # plt.title("signal_noise")
    #
    # plt.subplot(223)
    # plt.psd(realTemp - real)
    # plt.title("noise")
    #
    # plt.show()
    #
    # signal = real
    # signal_noise = realTemp
    # Ps = (np.linalg.norm(signal - signal.mean())) ** 2  # signal power
    # Pn = (np.linalg.norm(signal - signal_noise)) ** 2  # noise power
    #
    # print(f'信号功率 {Ps}')
    # print(f'噪声功率 {Pn}')
    # print(f'snr : {10 * np.log10(Ps / Pn)} dB')

    pass
