from base.model import *
from base.utils import *
from base.muldot import *
from sensor.sensors import *


dot1 = DotSet([
    Dot('dot1', subsequents=['dot3'], worker=BWT901CLInput()),
    # Dot('dot3', worker=PrintData(contents=['9_axis_dict']))
    # Dot('dot6', worker=Load(reappear=True), subsequents=['dot2'])
])

dot3 = Dot('dot3', worker=PrintData(contents=['9_axis_dict']))
# dot5 = Dot('dot5', worker=Save())


if __name__ == '__main__':
    # for i in range(500):
    #     dot1.run(Frame(end='dot1'))
    Mulignition([dot1, dot3]).run()

