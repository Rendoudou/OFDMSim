"""
@ 全局变量配置
@ 重要参数配置
"""

DEBUG = False  # 全局调试变量

# initial set up
OFDM_Carrier_Count = 200  # OFDM信号所携带的载波数目设置
Symbol_Per_Carrier = 10  # 每一个载波设置的符号数目
Bits_Per_Symbol = 4  # 每一个符号所带的信息量，4比特，默认用16QAM
SNR = 15  # 信噪比设置
