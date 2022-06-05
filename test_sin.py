from base.core import *
from base.utils import *
from sensor.connect_tools import *
from sensor.pars_tools import *
import numpy as np


class Sin(Worker):
    def __init__(self, name):
        super().__init__(name)
        self.i = 0.01

    def process(self, frame: Frame):
        frame.data['sin'] = np.sin(self.i)
        print(frame.data['sin'])
        self.i += 0.3

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
# task = NodeSet([
#     Node('dot0', subsequents=['dot1']),
#     Node('dot1', subsequents=['dot2', 'dot5']),
#     Node('dot2', subsequents=['dot3', 'dot4']),
#     Node('dot3'),
#     Node('dot4'),
#     Node('dot5'),
# ])


task = NodeSet([
    Node('dot0', subsequents=['dot1'], worker=Source()),
    Node('dot1', subsequents=['dot2', 'dot5'], worker=Sin('sin')),
    Node('dot2', subsequents=['dot3', 'dot4'], worker=Abs('abs')),
    Node('dot3', worker=PrintData('sin')),
    Node('dot4', worker=PoltData('plot')),
    Node('dot5'),
])


if __name__ == '__main__':
    # a = task.run(Frame(end='dot0'))
    # b = 0

    while True:
        a = task.run(Frame(end='dot0'))
