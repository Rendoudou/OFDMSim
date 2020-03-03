import matplotlib.pyplot as plt
import numpy as np

from PrimaryProcess import PrimaryProcess

#
# 主入口
#
if __name__ == "__main__":

    CorrectRatioBar = np.zeros(5)  # 1*250空数组

    for i in np.arange(0, 5):
        snr = i * 5.0
        tempCorrectRatio = PrimaryProcess(snr)
        CorrectRatioBar[i - 1] = tempCorrectRatio

    plt.figure(figsize=(16, 20))

    plt.subplot(111)
    ax = plt.plot(np.arange(0, 5) * 5.0, CorrectRatioBar)
    # ax.set_xlim([0, 25])
    plt.xlabel("SNR/dB")
    plt.ylabel("CorrectRatio")
    plt.grid(True)
    plt.show()

    pass
