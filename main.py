# This is a sample Python script.
import datetime
import os
import sys

import gen
from dic import stages, file_format
from util import format_date_time

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('+++++++ 数据生成 ++++++++')
    type = input('请选择阶段(默认ALL):\r\n'
                 + '0. ALL\r\n'
                 + '1. 升温\r\n'
                 + '2. 灭菌\r\n'
                 + '3. 干燥\r\n'
                 + '4. 冷却\r\n')
    if type == '':
        type = '0'

    format = input('请选择数据格式(默认txt):\r\n'
                 + '1. txt\r\n'
                 + '2. excel\r\n')
    if format == '':
        format = '1'

    base_time = input('请输入基准起始时间(HH:mm:SS格式):')
    if base_time == '':
        print('基准起始时间格式错误')
        sys.exit(0)

    data_cycle = input('请输入数据记录间隔(秒, 默认60s):')
    if data_cycle == '':
        data_cycle = 60

    sterilize_temperature = sterilize_temperature_fluctuate_range = sterilize_pressure = sterilize_pressure_fluctuate_range = cool_end_temperature = None
    heat_up_durative_time = sterilize_durative_time = dry_durative_time = cool_durative_time = 0

    if type == '0' or type == '1' or type == '2' or type == '3':
        sterilize_temperature = input('请输入灭菌温度(摄氏度, 默认121):')
        if sterilize_temperature == '':
            sterilize_temperature = 121.0
        sterilize_temperature_fluctuate_range = input('请输入灭菌温度波动范围(默认正负1.5):')
        if sterilize_temperature_fluctuate_range == '':
            sterilize_temperature_fluctuate_range = 1.5
        sterilize_pressure = input('请输入灭菌压力(KPA, 默认165):')
        if sterilize_pressure == '':
            sterilize_pressure = 165
        sterilize_pressure_fluctuate_range = input('请输入灭菌压力波动范围(默认正负5):')
        if sterilize_pressure_fluctuate_range == '':
            sterilize_pressure_fluctuate_range = 5

    # 升温阶段参数
    if type == '0' or type == '1':
        heat_up_durative_time = input('请输入升温持续时间(秒, 默认840s, 14分钟):')
        if heat_up_durative_time == '':
            heat_up_durative_time = 840

    # 灭菌阶段参数
    if type == '0' or type == '2':
        sterilize_durative_time = input('请输入灭菌持续时间(秒, 默认1800s, 30分钟):')
        if sterilize_durative_time == '':
            sterilize_durative_time = 1800

    # 干燥阶段参数
    if type == '0' or type == '3':
        dry_durative_time = input('请输入干燥持续时间(秒, 默认900s, 15分钟):')
        if dry_durative_time == '':
            dry_durative_time = 900

    # 冷却阶段参数
    if type== '0' or type == '4':
        cool_durative_time = input('请输入冷却持续时间(秒, 默认360s, 6分钟):')
        if cool_durative_time == '':
            cool_durative_time = 360
        #cool_end_temperature = input('请输入冷却截止温度(摄氏度):')

    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_' + stages.get(type) + "." + file_format.get(format)

    print('++++++++++++++++++++++')

    print('请确认:\r\n',
          '数据阶段:' + stages.get(type) + '\r\n',
          '数据格式:' + file_format.get(format) + '\r\n',
          '基准时间:' + base_time + '\r\n',
          '数据记录周期:' + str(data_cycle) + '秒\r\n',
          '灭菌温度:' + str(sterilize_temperature) + '摄氏度\r\n' if sterilize_temperature is not None else '',
          '灭菌温度波动范围(正负):' + str(sterilize_temperature_fluctuate_range) + '\r\n' if sterilize_temperature_fluctuate_range is not None else '',
          '灭菌压力:' + str(sterilize_pressure) + 'KPA\r\n' if sterilize_pressure is not None else '',
          '灭菌压力波动范围(正负):' + str(sterilize_pressure_fluctuate_range) + '\r\n' if sterilize_pressure_fluctuate_range is not None else '',
          '升温持续时间:' + str(heat_up_durative_time) + '秒\r\n' if int(heat_up_durative_time) > 0 else '',
          '灭菌持续时间:' + str(sterilize_durative_time) + '秒\r\n' if int(sterilize_durative_time) > 0 else '',
          '干燥持续时间:' + str(dry_durative_time) + '秒\r\n' if int (dry_durative_time) > 0 else '',
          '冷却持续时间:' + str(cool_durative_time) + '秒\r\n' if int (cool_durative_time) > 0 else ''
          #'冷却截止温度:' + str(cool_end_temperature) + '摄氏度\r\n' if cool_end_temperature is not None else ''
          )
    go_on = input("是否开始生成?(Y-开始, N-终止):")
    if go_on == 'N':
        print('已终止...')
        sys.exit()
    else:
        print('开始生成...')

    # 创建数据文件
    cur_dir = os.getcwd()
    file_name = cur_dir + os.sep + file_name
    file = open(file_name, mode = 'w+', encoding = 'utf-8', newline = '\n')
    # 输出文件头
    file.write('      工作开始:\r\n')
    file.write('      指 示 卡: 合格     不合格\r\n')
    file.write('      指示交代: 合格     不合格\r\n')
    file.write('      产品批号: \r\n')
    file.write('运转次数:\t\t\t   用户名:\r\n')
    file.write('灭菌温度:\t\t\t 灭菌时间:\r\n')
    file.write('程序性质:\t\t\t 干燥时间:\r\n')
    file.write('冷却温度:\t\t\t F0值设定:\r\n')
    file.write('* * * *  新华医疗  致力健康人生  * * * *\r\n')
    file.write('状态  时间    温度    压力kPA   F0值\r\n')


    # 处理时间
    base_time = format_date_time(base_time)

    match type:
        case '1':
            gen.heat_up(
                file,
                base_time,
                int(data_cycle),
                int(heat_up_durative_time),
                float(sterilize_temperature),
                float(sterilize_temperature_fluctuate_range),
                int(sterilize_pressure),
                int(sterilize_pressure_fluctuate_range)
            )
        case '2':
            gen.sterilize(
                file,
                base_time,
                int(data_cycle),
                int(sterilize_durative_time),
                float(sterilize_temperature),
                float(sterilize_temperature_fluctuate_range),
                int(sterilize_pressure),
                int(sterilize_pressure_fluctuate_range)
            )
        case '3':
            gen.dry(
                file,
                base_time,
                int(data_cycle),
                int(dry_durative_time),
                float(sterilize_temperature),
                float(sterilize_temperature_fluctuate_range),
                int(sterilize_pressure),
                int(sterilize_pressure_fluctuate_range)
            )
        case '4':
            gen.cool(
                file,
                base_time,
                int(data_cycle),
                int(cool_durative_time),
                float(sterilize_temperature),
                float(sterilize_temperature_fluctuate_range),
                int(sterilize_pressure),
                int(sterilize_pressure_fluctuate_range)
            )
        case _:
            gen.all(
                file,
                base_time,
                int(data_cycle),
                int(heat_up_durative_time),
                int(sterilize_durative_time),
                int(dry_durative_time),
                int(cool_durative_time),
                float(sterilize_temperature),
                float(sterilize_temperature_fluctuate_range),
                int(sterilize_pressure),
                int(sterilize_pressure_fluctuate_range)
            )

    file.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
