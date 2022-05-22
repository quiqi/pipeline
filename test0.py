from base.model import *
from base.utils import *
from sensor.connect_tools import *
from sensor.pars_tools import *
import numpy as np


dots1 = DotSet([
    Dot('head1', subsequents=['dot1']),
    Dot('dot1', subsequents=['dot2', 'dot5']),
    Dot('dot2', subsequents=['dot3', 'dot4']),
    Dot('dot3'),
    Dot('dot4', subsequents=['head2/dot4']),
    Dot('dot5'),
])

dots2 = DotSet([
    Dot('head2', subsequents=['dot1']),
    Dot('dot1', subsequents=['dot2', 'dot5']),
    Dot('dot2', subsequents=['dot3', 'dot4']),
    Dot('dot3'),
    Dot('dot4'),
    Dot('dot5'),
])

task = DotSet([
    dots1,
    dots2
])


if __name__ == '__main__':
    a = task.run(Frame(end='head1'))
    b = 0
