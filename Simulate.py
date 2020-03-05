import matplotlib.pyplot as plt
import numpy as np

from PrimaryProcess import primaryProcess
from BasicFunc import processBar
from tqdm import tqdm

from numba.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

from GlobalParameter import start, end, path, dis



#
# 主入口
#
if __name__ == "__main__":

    ErrorRatioBar = np.zeros(dis)  # 1*350空数组

    for i in tqdm(np.arange(start, end)):
        snr = i * path
        tempCorrectRatio = primaryProcess(snr)
        ErrorRatioBar[i - start] = tempCorrectRatio
        # processBar((i + 100) / 350, start_str='', end_str='100%', total_length=15)

    plt.figure(figsize=(8, 10))

    plt.subplot(111)
    plt.semilogy(np.arange(start, end) * path, ErrorRatioBar)  # y轴使用科学计数法
    # ax.set_xlim([0, 25])
    plt.xlabel("SNR/dB")
    plt.ylabel("BER")
    plt.grid(True)
    plt.show()

    pass
