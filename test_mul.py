import base.model as model
import base.utils as utils
from base.model import *
from base.utils import *
from base.muldot import *
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

    dot1 = Dot('dot0', subsequents=['dot1'])
    dot2 = DotSet([
        Dot('dot1', subsequents=['dot2'], worker=Sin('sin')),
        Dot('dot2', subsequents=['dot3'], worker=Abs('abs'))
    ])
    dot3 = Dot('dot3', worker=PrintData(contents=['sin']))

    Mulignition([dot1, dot2, dot3]).run()
