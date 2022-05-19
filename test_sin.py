from base.model import *
from base.utils import *
from sensor.port_listener import *
from sensor.sensor_data_parsing import *
import numpy as np


class Sin(Worker):
    def __init__(self, name):
        super().__init__(name)
        self.i = 0.01

    def process(self, frame: Frame):
        frame.data['sin'] = np.sin(self.i)
        print(frame.data['sin'])
        self.i += 0.1

        frame.info['_PLOT']['sin'] = frame.data['sin']

        return frame


class Abs(Worker):
    def __init__(self, name):
        super().__init__(name)

    def process(self, frame: Frame):
        frame.data['sin'] = abs(frame.data['sin'])
        frame.info['_PLOT']['sin'] = frame.data['sin']

        return frame


# test0中的框架
# task = DotSet([
#     Dot('dot0', subsequents=['dot1']),
#     Dot('dot1', subsequents=['dot2', 'dot5']),
#     Dot('dot2', subsequents=['dot3', 'dot4']),
#     Dot('dot3'),
#     Dot('dot4'),
#     Dot('dot5'),
# ])


task = DotSet([
    Dot('dot0', subsequents=['dot1'], worker=Source()),
    Dot('dot1', subsequents=['dot2', 'dot5'], worker=Sin('sin')),
    Dot('dot2', subsequents=['dot3', 'dot4']),
    Dot('dot3'),
    Dot('dot4', worker=PoltData('plot')),
    Dot('dot5'),
])


if __name__ == '__main__':
    # a = task.run(Frame(end='dot0'))
    # b = 0

    while True:
        a = task.run(Frame(end='dot0'))
