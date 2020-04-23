"""
@ OFDM仿真
@ 高斯信道 噪声
@ DD
"""

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


# #
# @ func: def awgn(signal, snr):
# @ 信号加噪声
# @ para signal 信号， snr 信噪比
# @ return 加噪结果
# #
def awgn(signal, snr):
    if len(signal.shape) > 1:
        noise = np.random.randn(signal.shape[0], signal.shape[1])  # 产生N(0,1)噪声数据
        noise = noise - np.mean(noise)  # 均值为0
        signal_power = np.linalg.norm(signal) ** 2 / signal.size  # 此处是信号的std**2
        noise_variance = signal_power / np.power(10, (snr / 10))  # 此处是噪声的std**2
        noise = (np.sqrt(noise_variance) / np.std(noise)) * noise  # 此处是噪声的std**2
        # noise_power = np.linalg.norm(noise) ** 2 / noise.size
        signal_noise = noise + signal
        return signal_noise

    elif len(signal.shape) == 1:
        return signal + wgn(signal, snr)


# #
# @ func: def AWGNComplex(real, imag, snr):
# @ 复数信号加噪声
# @ para signal 信号， snr 信噪比
# @ return 加噪结果 ,实部, 虚部
# #
def AWGNComplex(real, imag, snr):
    real_noise = awgn(real, snr)
    imag_noise = awgn(imag, snr)
    signal_complex = toComplex(real_noise, imag_noise)

    return signal_complex, real_noise, imag_noise


def AWGNComplex2(signal, snr):
    tempSignal = np.zeros((2, signal.shape[0]))
    tempSignal[0] = np.real(signal)
    tempSignal[1] = np.imag(signal)

    tempSignal_noise = awgn(tempSignal, snr)
    signalOut = tempSignal_noise[0] + tempSignal_noise[1] * 1j
    return signalOut.ravel()


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    a = np.random.randint(0, 2, 100)
    b = np.random.randint(0, 2, 100)
    c = a + b * 1j
    c_noise, a_noise, b_noise = AWGNComplex(a, b, 0)

    pass
