#
# ofdm仿真main
#
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

    PeBar = np.zeros((2, SNRDis), float)  # 误码率数组
    for i in tqdm(np.arange(SNRStart, SNREnd)):
        snr = i * SNRPath
        sum_symbol = 0
        sum_error = 0; sum_error_rec = 0
        while (sum_error < ErrorPerSNR) or (sum_error_rec < ErrorPerSNR):  # 最低误码基数限制
            error_temp, error_temp_rec = primaryProcess(snr)  # 仿真过程
            sum_error = sum_error + error_temp; sum_error_rec = sum_error_rec + error_temp_rec
            sum_symbol = sum_symbol + SymbolPerRound  # 每一轮测试的符号数目是相同的
            pass
        Pe = sum_error / sum_symbol; Pe_rec = sum_error_rec / sum_symbol
        PeBar[0, i - SNRStart] = Pe; PeBar[1, i - SNRStart] = Pe_rec
        # processBar((i + 100) / 350, start_str='', end_str='100%', total_length=15)
        pass

    plt.figure(figsize=(8, 6))
    plt.subplot(111)
    plt.semilogy(np.arange(SNRStart, SNREnd) * SNRPath, PeBar[0], color ='green', label ='ofdm_Pe_p')  # y轴使用科学计数法
    plt.semilogy(np.arange(SNRStart, SNREnd) * SNRPath, PeBar[1], color='red', label ='ofdm_Pe_p_rec')
    plt.legend()
    plt.xlabel("SNR/dB")
    plt.ylabel("BER")
    plt.title("OFDMSimulate")
    plt.grid(True)
    plt.show()

    pass
