"""
@ 全局变量配置
@ 重要参数配置
"""

from NextPow2 import nextPow2

DEBUG = False  # 全局调试变量
ObviousDeviation = True  # 明显偏移

# initial set up 初始设置
OFDMCarrierCount = 120  # 每个OFDM信号所携带的载波数目设置
PilotInterval = 3  # 三个符号插入一个导频，块状导频
Group = 4  # 一帧数据ofdm符号的组数
SymbolPerCarrier = PilotInterval * Group  # 每一个载波设置的符号数目，一帧要发送的ofdm符号数目,4组加载频的群
SymbolPerCarrier_Pilots = (PilotInterval + 1) * Group  # 添加导频后，一帧发送的ofdm符号变多
BitsPerSymbol = 4  # 每一个符号所带的信息量，4比特，默认用16QAM
IFFTLength = pow(2,nextPow2(OFDMCarrierCount) + 1)
PrefixRatio = 1 / 4  # 保护间隔与OFDM数据的比例 1/6~1/4
beta = 1 / 32  # 窗函数滚降系数
GI = int(PrefixRatio * IFFTLength)  # 每一个OFDM符号添加的循环前缀长度为1/4*IFFT_bin_length  即保护间隔长度为128
GIP = int(beta * (IFFTLength + GI))  # 循环后缀的长度20
SymbolLength = IFFTLength + GI + GIP  # 发送OFDM符号的实际长度
TxLength = SymbolPerCarrier * (IFFTLength + GI + GIP)  # 发送OFDM符号帧的实际长度
TxLength_Pilots = SymbolPerCarrier_Pilots * (IFFTLength + GI + GIP)  # 加入导频后发送同量信息的的长度

# 瑞利信道
Fd = 100  # HZ 最大多普勒频移

# 线性回归,机器学习
TrainingStep = 0.001  # 学习步长
MaxTrainingCycles = 300  # 梯度上升训练限制

# calc type 计算错误率的类型
CalcBitsError = True  # 是否计算误比特率

# sim set up 仿真设置
SNRStart = -10
SNREnd = 20
SNRPath = 1.0
SNRDis = SNREnd - SNRStart
ErrorPerSNR = 10000
SymbolPerRound = OFDMCarrierCount * SymbolPerCarrier * BitsPerSymbol
SymbolPerRound_Pilots = SymbolPerRound  # 实际信息位不变，频带利用率下降

# 16QAM映射图
mapping = {'0': (3, 3), '1': (1, 3), '2': (-3, 3), '3': (-1, 3),
           '4': (3, 1), '5': (1, 1), '6': (-3, 1), '7': (-1, 1),
           '8': (3, -3), '9': (1, -3), '10': (-3, -3), '11': (-1, -3),
           '12': (3, -1), '13': (1, -1), '14': (-3, -1), '15': (-1, -1)}

# # 16QAM映射图
# mapping = {'11': (-3, 3), '9': (-1, 3), '14': (1, 3), '15': (3, 3),
#            '10': (-3, 1), '8': (-1, 1), '12': (1, 1), '13': (3, 1),
#            '1': (-3, -1), '0': (-1, -1), '4': (1, -1), '6': (3, -1),
#            '3': (-3, -3), '2': (-1, -3), '5': (1, -3), '7': (3, -3)}

# # 16QAM映射图
# mapping = {'14': (-3, 3), '10': (-1, 3), '2': (1, 3), '6': (3, 3),
#            '15': (-3, 1), '11': (-1, 1), '3': (1, 1), '7': (3, 1),
#            '13': (-3, -1), '9': (-1, -1), '1': (1, -1), '5': (3, -1),
#            '12': (-3, -3), '8': (-1, -3), '0': (1, -3), '4': (3, -3)}

# # 16QAM映射图
# mapping = {'0': (-3, 3), '4': (-1, 3), '12': (1, 3), '8': (3, 3),
#            '1': (-3, 1), '5': (-1, 1), '13': (1, 1), '9': (3, 1),
#            '3': (-3, -1), '7': (-1, -1), '15': (1, -1), '11': (3, -1),
#            '2': (-3, -3), '6': (-1, -3), '14': (1, -3), '10': (3, -3)}
# 0000         0100           1100         1000
# 0001         0101           1101         1001
# 0011         0111           1111         1011
# 0010         0110           1110         1010
