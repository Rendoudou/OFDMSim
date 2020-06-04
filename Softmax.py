#
# 基于机器学习的ofdm仿真，softmax 实现
#
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from Pilot import pilotsPos, labels_16_classification

var_nums = 16  # 复杂模型加入隐藏层
classes = 16  # 16分类
show_frame = False


#
# 导入数据
#
def loadData(ofdm_awgn):
    pilots_awgn = ofdm_awgn[pilotsPos]  # 取出导频经信道后的结果
    pilots_awgn_re = pilots_awgn.reshape((-1, 1))  # 成为一列
    data = np.zeros((len(pilots_awgn_re), 2), float)
    data[:, 0] = pilots_awgn_re.real.ravel()  # 480*1 input 480
    data[:, 1] = pilots_awgn_re.imag.ravel()
    if show_frame:
        data_frame = DataFrame(data, columns=['实轴', '虚轴'])
        data_frame['标签'] = labels_16_classification.reshape((-1, 1))  # 新增一列
        pd.set_option('display.unicode.east_asian_width', True)  # 设置列名对齐
        print(data_frame)
        pass
    features = data
    labels = labels_16_classification.reshape((-1, 1))
    return features, labels

    # features = tf.constant(data)  # 特征
    # labels = tf.constant(labels_16_classification.reshape((-1, 1)))  # 标签
    #
    # data_set_db = tf.data.Dataset.from_tensor_slices((features, labels)).batch(32)  # 特征与标签一一对应,
    # return data_set_db


#
# 数据训练学习，全连接网络，学习率 0.2
#
def data_train_tensor(ofdm_awgn):
    features, labels = loadData(ofdm_awgn)  # 提取训练集 (N,2)数据集 （N，16）标签
    # 数据分类
    features_train = features[:-30]
    labels_train = labels[:-30]
    features_test = features[-30:]
    labels_test = labels[-30:]
    #数据类型转换
    features_train = tf.cast(features_train, tf.float32)
    features_test = tf.cast(features_test, tf.float32)


    train_set_db = tf.data.Dataset.from_tensor_slices((features_train,labels_train)).batch(32)
    test_set_db = tf.data.Dataset.from_tensor_slices((features_test, labels_test)).batch(32)

    # 截断型正态分布的随机数据,（2, var_nums）维度, 标准差为0.1
    w1 = tf.Variable(tf.random.truncated_normal([2, var_nums], stddev=0.1, seed=1))  # 第一层乘性系数 随机初始值
    b1 = tf.Variable(tf.random.truncated_normal([var_nums], stddev=0.1, seed=1))  # 第一层加性参数 随机初始值

    # 训练参数
    epoch = 50000
    lr = 0.5
    loss_all = 0
    train_loss_results = []  # 将每轮的loss记录在此列表中，为后续画loss曲线提供数据
    test_acc = []  # 将每轮的acc记录在此列表中，为后续画acc曲线提供数据

    # 训练网络，和测试网络
    for epoch in range(epoch):

        # 训练网络
        for step, (x_train, y_train) in enumerate(train_set_db):
            with tf.GradientTape() as tape:  # 梯度信息
                y = tf.matmul(x_train, w1) + b1  # 神经网络乘加运算
                y = tf.nn.softmax(y)  # 输出转换为
                y_one_hot = tf.one_hot(y_train, depth = classes)
                loss = tf.reduce_mean(tf.square(y_one_hot - y))
                loss_all += loss.numpy()
                pass
            grads = tape.gradient(loss, [w1, b1])
            w1.assign_sub(lr * grads[0])
            b1.assign_sub(lr * grads[1])
            pass

        print("Epoch {}, loss: {}".format(epoch, loss_all / 4))
        train_loss_results.append(loss_all / 4)  # 将4个step的loss求平均记录在此变量中
        loss_all = 0  # loss_all归零，为记录下一个epoch的loss做准备

        # 测试部分
        total_correct, total_number = 0, 0
        for x_test, y_test in test_set_db:
            # 使用更新后的参数进行预测
            y = tf.matmul(x_test, w1) + b1
            y = tf.nn.softmax(y)
            pred = tf.argmax(y, axis=0)  # 返回y中最大值的索引，即预测的分类
            # 将pred转换为y_test的数据类型
            pred = tf.cast(pred, dtype=y_test.dtype)
            # 若分类正确，则correct=1，否则为0，将bool型的结果转换为int型
            correct = tf.cast(tf.equal(pred, y_test), dtype=tf.int32)
            # 将每个batch的correct数加起来
            correct = tf.reduce_sum(correct)
            # 将所有batch中的correct数加起来
            total_correct += int(correct)
            # total_number为测试的总样本数，也就是x_test的行数，shape[0]返回变量的行数
            total_number += x_test.shape[0]
            pass
        #总的准确率等于total_correct/total_number
        acc = total_correct / total_number
        test_acc.append(acc)
        #print("Test_acc:", acc)
        #print("--------------------------")
        pass
    # 绘制 loss 曲线
    plt.title('Loss Function Curve')  # 图片标题
    plt.xlabel('Epoch')  # x轴变量名称
    plt.ylabel('Loss')  # y轴变量名称
    plt.plot(train_loss_results, label="$Loss$")  # 逐点画出trian_loss_results值并连线，连线图标是Loss
    plt.legend()  # 画出曲线图标
    plt.show()  # 画出图像

    # 绘制 Accuracy 曲线
    plt.title('Acc Curve')  # 图片标题
    plt.xlabel('Epoch')  # x轴变量名称
    plt.ylabel('Acc')  # y轴变量名称
    plt.plot(test_acc, label="$Accuracy$")  # 逐点画出test_acc值并连线，连线图标是Accuracy
    plt.legend()
    plt.show()

    pass


#
# debug
#
if __name__ == "__main__":
    pass
