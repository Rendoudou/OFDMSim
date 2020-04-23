"""
@ OFDM仿真
@ 找到下一个2的阶乘
@ DD
"""
import ctypes as ct


class FloatBits(ct.Structure):
    _fields_ = [
        ('M', ct.c_uint, 23),
        ('E', ct.c_uint, 8),
        ('S', ct.c_uint, 1)
    ]


class Float(ct.Union):
    _anonymous_ = ('bits',)
    _fields_ = [
        ('value', ct.c_float),
        ('bits', FloatBits)
    ]


# #
# @ def nextPow2(x):
# #
def nextPow2(x):
    """
    :param x: 输入数据
    :return: 比输入数据大的2的阶乘数
    """
    if x < 0:
        x = -x
    if x == 0:
        return 0
    d = Float()
    d.value = x
    if d.M == 0:
        return d.E - 127
    return d.E - 127 + 1


# #
# @ Debug(文件内)
# #
if __name__ == "__main__":
    print(nextPow2(10))
    pass
