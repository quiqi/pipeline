from base.core import *
from base.utils import *
from base.mul import *
from sensor.sensors import *


dot1 = NodeSet([
    Node('dot1', subsequents=['dot3'], worker=BWT901CLInput(port='com13')),
    # Node('dot3', worker=PrintData(contents=['9_axis_dict']))
    # Node('dot6', worker=Load(reappear=True), subsequents=['dot2'])
])

dot3 = Node('dot3', worker=PrintData(contents=['9_axis_dict']))
# dot5 = Node('dot5', worker=Save())

ws = WorkerSet('ws', [
    Source(),
    BWT901CLInput(port='com13'),
    PoltData('plot')
])


if __name__ == '__main__':
    # for i in range(500):
    #     dot1.run(Frame(end='dot1'))
    # MulIgnition([dot1, dot3]).run()
    while True:
        ws.run(Frame())

