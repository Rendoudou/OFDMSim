"""
@ OFDM仿真
@ 学习信道后,做出数据矫正
@ DD
"""
import numpy as np


#
# 得到畸变的原点
#
def getTransPoint(weights_x, weights_y):
    """
    :param weights_x: 畸变x
    :param weights_y: 畸变y
    :return: 变换后的原点
    """
    a = np.zeros((2, 2), float)
    a[0] = [weights_x[1], weights_x[2]]
    a[1] = [weights_y[1], weights_y[2]]

    b = np.zeros((2, 1), float)
    b[0] = -weights_x[0]
    b[1] = -weights_y[0]

    a_mat = np.mat(a)
    b_mat = np.mat(b)

    point_xy = a_mat.I * b_mat
    return np.array(point_xy).reshape((1, -1))


#
# 修正xy轴
#
def rectify(data, weiX, weiY):
    """
    :param data: 输入数据
    :param weiX: x轴参数
    :param weiY: y轴参数
    :return: 畸变矫正
    """
    data_x = data.real.ravel()
    data_y = data.imag.ravel()
    data_origin = np.ones((3, len(data_x)), float)
    data_origin[0] = data_x
    data_origin[1] = data_y

    weightsX = weiX.getA()  # mat矩阵转换
    weightsY = weiY.getA()

    zero_point = getTransPoint(weightsX, weightsY)  # 获得偏移的原点

    conformal_trans = np.zeros((3, 3), float)
    conformal_trans[0] = np.array([1.0, float(-weightsY[1] / weightsY[2]), zero_point[0][0]])
    conformal_trans[1] = np.array([float(-weightsX[2] / weightsX[1]), 1.0, zero_point[0][1]])
    conformal_trans[2] = np.array([0, 0, 1])

    data_out_temp = np.mat(conformal_trans).I * np.mat(data_origin)

    data_out_r = (data_out_temp[0]).reshape(data.shape)
    data_out_i = (data_out_temp[1]).reshape(data.shape)
    data_out = data_out_r + data_out_i * 1j

    return np.array(data_out)


#
# debug
#
if __name__ == "__main__":
    zero_point = np.ones((2, 1))
    print(zero_point[1,0])
    weightsY = np.ones((3, 1), float)
    conformal_trans = np.zeros((3, 3), float)
    conformal_trans[0] = np.array([1.0, float(-weightsY[1] / weightsY[2]), float(zero_point[0])])
    pass
