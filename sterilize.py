# 灭菌信息


class Sterilize:

    # 构造函数
    def __init__(self, stage, time, temperature, pressure, f0):
        self.stage = stage
        self.time = time
        self.temperature = temperature
        self.pressure = pressure
        self.f0 = f0

    # 设置f0
    def f0(self, f0):
        self.f0 = f0
