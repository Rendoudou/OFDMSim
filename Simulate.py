import matplotlib.pyplot as plt
import numpy as np

from PrimaryProcess import PrimaryProcess

import imtoolkit

#
# 主入口
#
if __name__ == "__main__":

    CorrectRatioBar = np.zeros(250)  # 1*250空数组

    for i in np.arange(1, 251):
        snr = i * 0.1
        tempCorrectRatio = PrimaryProcess(snr)
        CorrectRatioBar[i - 1] = tempCorrectRatio

    plt.figure(figsize=(16, 20))

    plt.subplot(111)
    ax = plt.plot(np.arange(1, 251) * 0.1, CorrectRatioBar)
    # ax.set_xlim([0, 25])
    plt.xlabel("SNR/dB")
    plt.ylabel("CorrectRatio")
    plt.grid(True)
    plt.show()

    pass
