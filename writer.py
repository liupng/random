# 输出数据到文件


# 文件头: 时间 ｜ 温度 | 压力 | F0值


def output(file, data, stage):
    i = 0
    for d in data:
        if i == 0:
            file.write(str(stage) + '  ' + d.time.strftime('%H:%M:%S') + '    ' + '{:0>5.1f}'.format(d.temperature) + '    ' + '{:04}'.format(
                d.pressure) + '   ' + '{:0>5.1f}'.format(d.f0) + '\r\n')
        else:
            file.write('    ' + '  ' + d.time.strftime('%H:%M:%S') + '    ' + '{:0>5.1f}'.format(d.temperature) + '    ' + '{:04}'.format(
                d.pressure) + '   ' + '{:0>5.1f}'.format(d.f0) + '\r\n')
        i+=1