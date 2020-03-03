"""
@ OFDM仿真
@ 分析 错误率
@ DD
"""

import numpy as np
from GlobalParameter import CalcBitsError


# #
# @ def calcMismatchRatio(a, b):
# @ 计算误码率或者误比特率
# @ para a 源信息，b 接收端信息
# @ return errorRatio 错误率
# #
def calcMismatchRatio(a, b):

    length = min(len(a),len(b))
    count = 0.0

    if CalcBitsError:
        for i in np.arange(length):

            if a[i] != b[i]:
                count = count + 1.0
                pass

        return count / length
    else:
        tempA = np.zeros(4)
        tempB = np.zeros(4)
        for i in np.arange(int(length / 4)):
            tempA = a[i * 4: i * 4 + 4]
            tempB = b[i * 4: i * 4 + 4]
            if np.array_equal(tempA, tempB):
                pass
            else:
                count = count + 1.0
                pass
            pass

        return count / (float(length / 4.0))


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":

    a = np.array([1, 2, 3])
    b = np.array([1, 2, 3])
    print((a[1:2] == b[1:2]).all())
    a = np.array([3, 2, 1])
    b = np.array([1, 2, 3])
    print((a == b).all())

    pass
