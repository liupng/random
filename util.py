# 各种工具函数

import datetime
import math

import numpy as np


# 指定日期时分秒
def format_date_time(base_time):
    base_date_time = datetime.datetime.now()
    time_array = base_time.split(':')
    base_date_time = datetime.datetime(base_date_time.year, base_date_time.month, base_date_time.day, int(time_array[0]),
                                       int(time_array[1]), int(time_array[2]))
    return base_date_time


# 升温区间温度函数1(对数函数曲线)
def heat_temperature1(index, target):
    temperature = 54.897 * np.log(index + 2) - 10.394
    # 二次随机浮动
    temperature = random_float(temperature, -0.2, 0.2)
    if temperature > target:
        temperature = target
    return float('%.1f' % temperature)


# 升温区间温度函数2(S曲线)
def heat_temperature(index, target):
    # 优先用指数函数
    if index < 2:
        index = 2
    temperature = 14.24 * np.exp(0.2639 * index)
    if temperature > 85:
        # 超过范围用对数函数
        temperature = 17.821 * np.log(index-6) + 85.09

    temperature = random_float(temperature, 0.2, 0.2)
    return float('%.1f' % temperature)


# 灭菌区间温度函数
def ster_temperature(base, low, up):
    temperature = random_float(base, low, up)
    if temperature > (base + up):
        return base + up
    return temperature


# 干燥区间温度函数
def dry_temperature(index, base, direct, cycle=0):
    temperature = 124.96 * np.power(index + 1 - 12 * cycle, -0.085)
    temperature = random_float(temperature, 0.5, 0.2)
    if temperature > base:
        temperature = base
        return float('%.1f' % temperature), direct, cycle
    # 低于98度,转升温
    if direct == 0 and temperature <= 98.0:
        direct = 1
    if direct > 0:
        direct += 1
        temperature = 4.3359 * np.log(direct) + 98.205
        # 升温到104度, 继续转降温
        if temperature > 104.0:
            direct = 0
            cycle += 1
    temperature = random_float(temperature, 0.5, 0.2)
    return float('%.1f' % temperature), direct, cycle


# 冷却区间温度函数
def cool_temperature(index, base, cool_end_temperature):
    if cool_end_temperature == 50.0:
        temperature = -13.33 * np.log(index + 1) + 103.86
    else:
        temperature = -3.3393 * (index + 1) + 103.49
    temperature = random_float(temperature, 0.5, 0.2)
    abort = False
    if temperature > base:
        temperature = base
    if temperature < cool_end_temperature:
        temperature = random_float(cool_end_temperature, 0, 0.2)
        abort = True
    return float('%.1f' % temperature), abort


# 计算F0值
def cal_f0(data, last_f0, base_temperature, cur_temperature, data_cycle):
    # 低于100度,直接取前一个值
    if cur_temperature < 100.0:
        return last_f0

    # 高于100度进行计算
    cur_f0 = (data_cycle/60) * np.power(10, (cur_temperature - base_temperature)/10)
    if len(data) == 0:
        f0 = last_f0 + cur_f0
    else:
        f0 = data[-1].f0 + cur_f0

    return float('%.1f' % f0)


# 指定区间内float随机数
def random_float(base, low, up):
    lower = float(base) - float(low)
    upper = float(base) + float(up)
    random_float = np.random.uniform(lower, upper)
    return float('%.1f' % random_float)


# 指定区间的int随机数
def random_int(base, start = 0, end = 0):
    lower = int(base) + int(start)
    upper = int(base) + int(end)
    return np.random.randint(lower, upper)


# 计算区间
def section(durative_time, cycle):
    return math.floor(int(durative_time) / int(cycle))


if __name__ == '__main__':
    '''
    data_cycle = 60
    cur_temperature = 122
    base_temperature = 121
    last_f0 = 39.2

    # 高于100度进行计算
    cur_f0 = (data_cycle / 60) * np.power(10, (cur_temperature - base_temperature) / 10)
    f0 = last_f0 + cur_f0

    print(str(float('%.1f' % f0)))
    '''
    '''
    sterilize_temperature = 121.0
    sterilize_temperature_fluctuate_range = 1.5
    temp = temperature = random_float(sterilize_temperature, 0, sterilize_temperature_fluctuate_range, 1)
    print(str(float('%.1f' % temp)))
    '''

    # print(heat_temperature(1, 121.0))

    index = 50
    print(float(index) == 50.0)
    # print(-13.33 * np.log(index) + 103.86)
    # print(-0.0003 * np.power(index, 3) + 0.0383 * np.power(index, 2) - 2.0323 * index + 94.058)
    # print(-1 * np.power(10, 0.00001 * np.power(index, 4)) - 0.0016 * np.power(index, 3) + 0.0919 * np.power(index, 2) - 2.8213 * index + 96.801)
