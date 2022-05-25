from base.model import *
from base.utils import *
from sensor.connect_tools import *
from sensor.pars_tools import *
import numpy as np


dots1 = DotSet([
    Dot('head2', subsequents=['dot1']),
    Dot('dot1', subsequents=['dot2']),
    Dot('dot2', subsequents=['dot3']),
    Dot('dot3', subsequents=['dot4', 'dot5']),
    Dot('dot4'),
    Dot('dot5'),
])

dots1 = DotSet([
    Dot('head2', subsequents=['dot1']),
    Dot('dot1', subsequents=['dot2'], worker=Source()),
    Dot('dot2', subsequents=['dot3'], worker=PortListener('port')),
    Dot('dot3', subsequents=['dot4', 'dot5'], worker=BWT901CL('b')),
    Dot('dot4', worker=PrintData('print', [])),
    Dot('dot5', worker=PoltData('Polt')),
])

task = DotSet([
    dots1,
    dots2
])


if __name__ == '__main__':
    # dots1.run(Frame(end='head1'))
    Mulignition([dots1, dots2]).run()

