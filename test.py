from base.model import *
from base.utils import *
from base.muldot import *
from sensor.port_listener import *
from sensor.sensor_data_parsing import *


dot1 = DotSet([
    Dot('dot1', subsequents=['dot2'], worker=PortListener('bwt901cl_listener')),
    Dot('dot2', subsequents=['dot3'], worker=BWT901CL()),
    # Dot('dot6', worker=Load(reappear=True), subsequents=['dot2'])
])

dot3 = Dot('dot3', worker=PrintData(contents=['9_axis_dict']))
# dot5 = Dot('dot5', worker=Save())


if __name__ == '__main__':
    # for i in range(500):
    #     task.run(Frame(end='dot0'))
    Mulignition([dot1, dot3]).run()

