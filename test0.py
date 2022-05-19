from base.model import *
from base.utils import *
from sensor.port_listener import *
from sensor.sensor_data_parsing import *
import numpy as np

task = DotSet([
    Dot('dot0', subsequents=['dot1']),
    Dot('dot1', subsequents=['dot2', 'dot5']),
    Dot('dot2', subsequents=['dot3', 'dot4']),
    Dot('dot3'),
    Dot('dot4'),
    Dot('dot5'),
])


if __name__ == '__main__':
    a = task.run(Frame(end='dot0'))
    b = 0
