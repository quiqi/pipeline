from base.model import *
from base.utils import *
from sensor.port_listener import *
from sensor.sensor_data_parsing import *


task = DotSet([
    Dot('dot0', subsequents=['dot1'], worker=Source()),
    Dot('dot1', subsequents=['dot2', 'dot5'], worker=PortListener('bwt901cl_listener')),
    Dot('dot2', subsequents=['dot3', 'dot4'], worker=BWT901CL(), send_mod='copy'),
    Dot('dot3', worker=PrintData(contents=['9_axis_dict'])),
    Dot('dot4', worker=PoltData('plot')),
    # Dot('dot5', worker=Save()),
    # Dot('dot6', worker=Load(reappear=True), subsequents=['dot2'])
])


if __name__ == '__main__':
    for i in range(500):
        task.run(Frame(end='dot0'))
