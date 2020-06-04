"""
@ 基于机器学习的OFDM仿真
@ 机器学习改善信道估计，主要是线性回归计算最合适的X&Y轴，修正接收信号。
@ DD
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from GlobalParameter import MaxTrainingCycles, TrainingStep
from Pilot import labels_2_classification, pilotsPos
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

font = {'family':'SimHei'}  # 设置使用的字体（需要显示中文的时候使用）
matplotlib.rc('font',**font)  # 设置显示中文，与字体配合使用
matplotlib.rcParams['axes.unicode_minus']=False

figSeq = 1


#
# 画出分类结果,y值分界线
#
def plotBestFit_x(wei, dataMat, labelMat):
    """
    :param wei: 分界线参数
    :param dataMat: 数据集合
    :param labelMat: 标签集合
    :return: 画图
    """
    global figSeq
    weights = wei.getA()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
        pass
    x = np.arange(-5.0, 5.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    # ax.scatter(xcord2, ycord2, s=30, c='green')
    # ax.plot(x, y)
    # plt.grid(True)
    # plt.title('分类器模型一')
    # plt.xlabel('real'); plt.ylabel('imag')
    # plt.show()

    return x, y


#
# 画出分类结果,x值分界线
#
def plotBestFit_y(wei, dataMat, labelMat):
    """
    :param wei: 分界线参数
    :param dataMat: 数据集合
    :param labelMat: 标签集合
    :return: 画图
    """
    global figSeq
    weights = wei.getA()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
        pass
    y = np.arange(-5.0, 5.0, 0.1)
    x = -(y * weights[2] + weights[0]) / weights[1]

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    # ax.scatter(xcord2, ycord2, s=30, c='green')
    # ax.plot(x, y)
    # plt.grid(True)
    # plt.title('分类器模型二')
    # plt.xlabel('real'); plt.ylabel('imag')
    # plt.show()
    return x, y


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

    x_labels = labels_2_classification[:, :, 0].reshape((-1, 1))
    y_labels = labels_2_classification[:, :, 1].reshape((-1, 1))
    return data, x_labels, y_labels


#
# 阶跃函数
#
def sigmoid(inx):
    s = 1 / (1 + np.exp(-inx))
    return s


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
    m, n = np.shape(dataMatrix)  # m * n
    weights = np.ones((n, 1))  # n * 1
    for i in np.arange(maxCycle):
        h = sigmoid(dataMatrix * weights)  # m * 1
        error = labelMat - h  # m * 1
        weights = weights + alpha * dataMatrix.transpose() * error  # w + al * (n * m) * (m * 1)
        pass

    return weights


#
# 画出畸变的X轴和Y轴
#
def plotXY(x1, y1, x2, y2, data):
    """
    :param data:
    :param x1: 有关直线的数组
    :param y1:
    :param x2:
    :param y2:
    :return: 畸变的xy轴
    """
    plt.figure()
    plt.plot(x1, y1, color='red', label='x-axis')
    plt.plot(x2, y2, color='green', label='y-axis')
    plt.scatter(data[:, 1], data[:, 2], color='blue')
    plt.xlabel('real')
    plt.ylabel('imag')
    plt.title('训练后的实轴与虚轴')
    plt.legend()
    plt.grid()
    plt.show()
    pass


#
# 训练新坐标轴
#
def trainAxis(ofdm_awgn):
    """
    :param ofdm_awgn: 输入参数在流程上是,ofdm信号经过信道后,经串并转换,fft,去补零成分后的结果。
    :return: 训练结果
    """
    data, x_label, y_label = loadData(ofdm_awgn)
    weights_x = gradAscent(data, x_label)  # 梯度上升,线性回归,训练xy轴
    weights_y = gradAscent(data, y_label)
    x_x, x_y = plotBestFit_x(weights_y, data, y_label)  # 区分y的正负，画出矫正的x轴
    y_x, y_y = plotBestFit_y(weights_x, data, x_label)  # 区分x的正负，画出矫正的y轴
    plotXY(x_x, x_y, y_x, y_y, data)

    return weights_x, weights_y


#
# debug
#
if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()  # 保证sess.run()能够正常运行
    hello = tf.constant('hello,tensorflow')
    sess = tf.compat.v1.Session()  # 版本2.0的函数
    print(sess.run(hello))

    pass
