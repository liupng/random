# 生成各个阶段的数据
import math

import writer
from sterilize import Sterilize
from util import random_int, random_float, section, heat_temperature, dry_temperature, \
    cool_temperature, cal_f0, ster_temperature
from datetime import timedelta


# 升温阶段
def heat_up(file, base_time, data_cycle, heat_up_durative_time, sterilize_temperature,
            sterilize_temperature_fluctuate_range, sterilize_pressure, sterilize_pressure_fluctuate_range, last_f0 = 0.0):
    print('开始生成升温阶段数据')
    count = section(heat_up_durative_time, data_cycle)
    data = []
    target = random_float(sterilize_temperature, -0.2 * sterilize_temperature_fluctuate_range, 0)
    # 生成数据
    for i in range(0, count):
        if i == 0:
            time = base_time + timedelta(seconds = random_int(10, end = data_cycle * 0.5))
            pressure = 0
        else:
            time = base_time + timedelta(seconds = i * data_cycle)
            pressure = random_int(sterilize_pressure, end = sterilize_pressure_fluctuate_range)
        temperature = heat_temperature((i+1), target)
        # 如果温度高于sterilize_temperature, 则应该转入灭菌阶段
        if temperature > sterilize_temperature:
            break
        last_f0 = cal_f0(data, last_f0, sterilize_temperature, temperature, data_cycle)
        data.append(Sterilize('升温', time, temperature, pressure, last_f0))
        # 输出到文件中
    writer.output(file, data, '升温')
    return data


# 灭菌阶段
def sterilize(file, base_time, data_cycle, sterilize_durative_time, sterilize_temperature,
              sterilize_temperature_fluctuate_range, sterilize_pressure, sterilize_pressure_fluctuate_range, last_f0 = 0.0):
    print('开始生成灭菌阶段数据')
    count = section(sterilize_durative_time, data_cycle)
    data = []
    # 生成数据
    for i in range(0, count + 1):
        if i == 0:
            time = base_time + timedelta(seconds = random_int(3, 0, 5))
            temperature = random_float(121.0, 0, 0.1)
        else:
            time = base_time + timedelta(seconds = i * data_cycle)
            temperature = ster_temperature(sterilize_temperature, 0, sterilize_temperature_fluctuate_range)
        pressure = random_int(sterilize_pressure, start = -0.5 * sterilize_pressure_fluctuate_range, end = sterilize_pressure_fluctuate_range)
        last_f0 = cal_f0(data, last_f0, sterilize_temperature, temperature, data_cycle)
        data.append(Sterilize('灭菌', time, temperature, pressure, last_f0))
    # 输出到文件中
    writer.output(file, data, '灭菌')
    return data


# 干燥阶段
def dry(file, base_time, data_cycle, dry_durative_time, sterilize_temperature, sterilize_temperature_fluctuate_range,
        sterilize_pressure, sterilize_pressure_fluctuate_range, last_f0 = 0.0):
    print('开始生成干燥阶段数据')
    count = section(dry_durative_time, data_cycle)
    data = []
    direct = 0
    cycle = 0
    base_temperature = random_float(sterilize_temperature, sterilize_temperature_fluctuate_range, 0)
    # 生成数据
    for i in range(0, count + 1):
        if i == 0:
            time = base_time + timedelta(seconds = random_int(3, 0, 5))
        else:
            time = base_time + timedelta(seconds = i * data_cycle)
        temperature, direct, cycle = dry_temperature(i, base_temperature, direct, cycle)
        pressure = random_int(sterilize_pressure, start = -1 * sterilize_pressure_fluctuate_range, end = sterilize_pressure_fluctuate_range)
        last_f0 = cal_f0(data, last_f0, sterilize_temperature, temperature, data_cycle)
        data.append(Sterilize('干燥', time, temperature, pressure, last_f0))
    '输出到文件中'
    writer.output(file, data, '干燥')
    return data


# 冷却阶段
def cool(file, base_time, data_cycle, cool_durative_time, sterilize_temperature, sterilize_temperature_fluctuate_range,
         sterilize_pressure, sterilize_pressure_fluctuate_range, cool_end_temperature, last_f0=0.0):
    print('开始生成冷却阶段数据')
    count = section(cool_durative_time, data_cycle)
    data = []
    base_temperature = random_float(sterilize_temperature, sterilize_temperature_fluctuate_range, 0)
    # 生成数据
    for i in range(0, count + 1):
        if i == 0:
            time = base_time + timedelta(seconds = random_int(3, 0, 5))
        else:
            time = base_time + timedelta(seconds = i * data_cycle)
        temperature, abort = cool_temperature(i, base_temperature, cool_end_temperature)
        pressure = random_int(sterilize_pressure, start = -1 * sterilize_pressure_fluctuate_range, end = 0)
        last_f0 = cal_f0(data, last_f0, sterilize_temperature, temperature, data_cycle)
        data.append(Sterilize('冷却', time, temperature, pressure, last_f0))
        if abort:
            break
    # 输出到文件中
    writer.output(file, data, '冷却')
    return data


# 排气阶段
def exsufflate(file, base_time, data_cycle, sterilize_temperature, cool_temperature, cool_temperature_fluctuate_range, cool_pressure,
               cool_pressure_fluctuate_range, last_f0 = 0.0):
    print('开始生成排气阶段数据')
    data = []
    temperature = cool_temperature
    # 生成数据
    for i in range(0, 2):
        if i == 0:
            time = base_time + timedelta(seconds=random_int(10, end = data_cycle * 0.5))
            pressure = random_int(cool_pressure, start=-1 * cool_pressure_fluctuate_range, end=0)
        else:
            time = base_time + timedelta(seconds=i * data_cycle)
            pressure = random_int(45, start=-1* cool_pressure_fluctuate_range, end=cool_pressure_fluctuate_range)
        temperature = random_float(temperature, cool_temperature_fluctuate_range, 0)
        last_f0 = cal_f0(data, last_f0, sterilize_temperature, temperature, data_cycle)
        data.append(Sterilize('排气', time, temperature, pressure, last_f0))
    # 输出到文件中
    writer.output(file, data, '排气')
    return data


# 结束阶段
def end(file, base_time, data_cycle, sterilize_temperature, exsufflate_temperature, exsufflate_temperature_range, last_f0 = 0.0):
    print('开始生成结束阶段数据')
    data = []
    time = base_time + timedelta(seconds=random_int(30, end = data_cycle * 0.8))
    temperature = random_float(exsufflate_temperature, exsufflate_temperature_range, 0)
    pressure = random_int(17, start = -1 * exsufflate_temperature_range, end = 0)
    last_f0 = cal_f0(data, last_f0, sterilize_temperature, temperature, data_cycle)
    data.append(Sterilize('结束', time, temperature, pressure, last_f0))
    # 输出到文件中
    writer.output(file, data, '结束')
    return data


# 全部阶段
def all(file, base_time, data_cycle, heat_up_durative_time, sterilize_durative_time, dry_durative_time,
        cool_durative_time, sterilize_temperature, sterilize_temperature_fluctuate_range, sterilize_pressure,
        sterilize_pressure_fluctuate_range, cool_end_temperature):
    # 升温
    data = heat_up(file, base_time, data_cycle, heat_up_durative_time, sterilize_temperature,
                   sterilize_temperature_fluctuate_range, sterilize_pressure, sterilize_pressure_fluctuate_range)

    # 灭菌
    last_data = data[-1]
    base_time = last_data.time
    base_temperatue = sterilize_temperature
    last_f0 = last_data.f0
    data = sterilize(file, base_time, data_cycle, sterilize_durative_time, base_temperatue,
              sterilize_temperature_fluctuate_range, sterilize_pressure, sterilize_pressure_fluctuate_range, last_f0)

    # 干燥
    last_data = data[-1]
    base_time = last_data.time
    base_temperatue = data[-1].temperature
    last_f0 = last_data.f0
    data = dry(file, base_time, data_cycle, dry_durative_time, base_temperatue, sterilize_temperature_fluctuate_range,
        sterilize_pressure, sterilize_pressure_fluctuate_range, last_f0)

    # 冷却
    last_data = data[-1]
    base_time = last_data.time
    base_temperatue = data[-1].temperature
    last_f0 = last_data.f0
    data = cool(file, base_time, data_cycle, cool_durative_time, base_temperatue, sterilize_temperature_fluctuate_range,
                sterilize_pressure, sterilize_pressure_fluctuate_range, cool_end_temperature, last_f0)

    # 排气
    last_data = data[-1]
    base_time = last_data.time
    base_temperatue = data[-1].temperature
    last_f0 = last_data.f0
    data = exsufflate(file, base_time, data_cycle, sterilize_temperature, base_temperatue, sterilize_temperature_fluctuate_range,
               sterilize_pressure, sterilize_pressure_fluctuate_range, last_f0)

    # 结束
    last_data = data[-1]
    base_time = last_data.time
    base_temperatue = data[-1].temperature
    last_f0 = last_data.f0
    end(file, base_time, data_cycle, sterilize_temperature, base_temperatue, sterilize_pressure_fluctuate_range, last_f0)