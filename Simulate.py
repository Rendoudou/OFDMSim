import warnings

import matplotlib.pyplot as plt
import numpy as np
from numba.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
from tqdm import tqdm

from GlobalParameter import SNRStart, SNREnd, SNRPath, SNRDis, ErrorPerSNR, SymbolPerRound
from PrimaryProcess import primaryProcess

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)


#
# 主入口
#
if __name__ == "__main__":

    ErrorRatioBar = np.zeros(SNRDis)  # 1*250空数组
    for i in tqdm(np.arange(SNRStart, SNREnd)):
        snr = i * SNRPath
        tempTestSymbolSum = 0
        tempErrorSum = 0
        while tempErrorSum < ErrorPerSNR:
            tempErrorCount = primaryProcess(snr)  # 仿真过程
            tempErrorSum = tempErrorSum + tempErrorCount
            tempTestSymbolSum = tempTestSymbolSum + SymbolPerRound
            pass
        tempErrorRatio = tempErrorSum / tempTestSymbolSum
        ErrorRatioBar[i - SNRStart] = tempErrorRatio
        # processBar((i + 100) / 350, start_str='', end_str='100%', total_length=15)

    plt.figure(figsize=(8, 6))

    plt.subplot(111)
    plt.semilogy(np.arange(SNRStart, SNREnd) * SNRPath, ErrorRatioBar)  # y轴使用科学计数法
    # ax.set_xlim([0, 25])
    plt.xlabel("SNR/dB")
    plt.ylabel("BER")
    plt.title("OFDMSimulate with CP")
    plt.grid(True)
    plt.show()

    pass
