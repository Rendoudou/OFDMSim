"""
@ 基于机器学习的OFDM仿真
@ 机器学习改善信道估计，主要是线性回归计算最合适的X&Y轴，修正接收信号。
@ DD
"""
import numpy as np
import matplotlib.pyplot as plt

from Pilot import pilots, labels, pilotsPos, pilotsNeed
from GlobalParameter import MaxTrainingCycles,TrainingStep

figSeq = 1

#
# 画出分类结果
#
def plotBestFit_y(wei, dataMat, labelMat):
    """
    :param weights: 分界线参数
    :param dataMat: 数据集合
    :param labelMat: 标签集合
    :return: 画图
    """
    global figSeq
    weights = wei.getA()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure(figSeq)
    figSeq = figSeq + 1
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-4.0, 4.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('real'); plt.ylabel('imag')
    plt.show()
    pass


def plotBestFit_x(wei, dataMat, labelMat):
    """
    :param weights: 分界线参数
    :param dataMat: 数据集合
    :param labelMat: 标签集合
    :return: 画图
    """
    global figSeq
    weights = wei.getA()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure(figSeq)
    figSeq = figSeq + 1
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    y = np.arange(-4.0, 4.0, 0.1)
    x = -(y * weights[2] + weights[0]) / weights[1]
    ax.plot(x, y)
    plt.xlabel('real'); plt.ylabel('imag')
    plt.show()
    pass


#
# 载入训练数据
#
def loadData(ofdm_awgn):
    """
    :param ofdm_awgn: 输入参数在流程上是,ofdm信号经过信道后,经串并转换,fft,去补零成分后的结果。
    :return: 当前训练数据，数据标签
    """
    pilots_awgn = ofdm_awgn[pilotsPos]  # 取出导频经信道后的结果
    pilots_awgn_re = pilots_awgn.reshape((-1, 1))  # 成为一列
    data = np.zeros((len(pilots_awgn_re), 3))
    for i in np.arange(len(pilots_awgn_re)):
        data[i, :] = np.array([1.0, pilots_awgn_re[i].real, pilots_awgn_re[i].imag])
        pass

    x_labels = labels[:, :, 0].reshape((-1,1))
    y_labels = labels[:, :, 1].reshape((-1,1))
    return data, x_labels, y_labels


#
# 阶跃函数
#
def sigmoid(inX):
    return 1.0 / (1 + np.exp(-inX))


#
# 梯度上升训练
#
def gradAscent(dataMatIn, classLabels):
    """
    :param dataMatIn: 输入训练参数
    :param classLabels: 输入训练参数对应的标签
    :return: 最佳分割线数据
    """
    maxCycle = MaxTrainingCycles
    alpha = TrainingStep
    dataMatrix = np.mat(dataMatIn)  # m * n
    labelMat = np.mat(classLabels)  # m * 1
    m, n = np.shape(dataMatrix) # m * n
    weights = np.ones((n, 1))  # n * 1
    for i in np.arange(maxCycle):
        h = sigmoid(dataMatrix * weights)  # m * 1
        error = labelMat - h  # m * 1
        weights = weights + alpha * dataMatrix.transpose() * error  # w + al * (n * m) * (m * 1)
        pass

    return weights


#
# 训练新坐标轴
#
def trainAxis(ofdm_awgn):
    """
    :param ofdm_awgn: 输入参数在流程上是,ofdm信号经过信道后,经串并转换,fft,去补零成分后的结果。
    :return: 训练结果
    """
    data, x_label, y_label = loadData(ofdm_awgn)
    weights_x = gradAscent(data, x_label)  # 梯度上升，线性回归
    weights_y = gradAscent(data, y_label)
    plotBestFit_x(weights_x, data, x_label)
    plotBestFit_y(weights_y, data, y_label)

    return weights_x, weights_y


#
# debug
#
if __name__ == "__main__":
    figSeq += 1
    print(figSeq)
    pass