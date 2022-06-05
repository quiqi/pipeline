import base.core as model
import base.utils as utils
from base.core import *
from base.utils import *
from base.mul import *
import numpy as np


class Sin(model.Worker):
    def __init__(self, name):
        super().__init__(name)
        self.i = 0.01

    def process(self, frame: model.Frame):
        frame.data['sin'] = np.sin(self.i)
        # print(frame.data['sin'])
        self.i += 0.3

        frame.info['_PLOT']['sin'] = frame.data['sin']
        return frame


class Abs(model.Worker):
    def __init__(self, name):
        super().__init__(name)

    def process(self, frame: model.Frame):
        frame.data['sin'] = abs(frame.data['sin'])
        frame.info['_PLOT']['sin'] = frame.data['sin']

        return frame


if __name__ == '__main__':

    dot1 = Node('dot0', subsequents=['dot1'])
    dot2 = NodeSet([
        Node('dot1', subsequents=['dot2'], worker=Sin('sin')),
        Node('dot2', subsequents=['dot3'], worker=Abs('abs'))
    ])
    dot3 = Node('dot3', worker=PrintData(contents=['sin']))

    MulIgnition([dot1, dot2, dot3]).run()
