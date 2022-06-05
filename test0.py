from base.core import *
from base.utils import *
from sensor.connect_tools import *
from sensor.pars_tools import *
import numpy as np


dots1 = NodeSet([
    Node('head2', subsequents=['dot1']),
    Node('dot1', subsequents=['dot2']),
    Node('dot2', subsequents=['dot3']),
    Node('dot3', subsequents=['dot4', 'dot5']),
    Node('dot4'),
    Node('dot5'),
])

dots1 = NodeSet([
    Node('head2', subsequents=['dot1']),
    Node('dot1', subsequents=['dot2'], worker=Source()),
    Node('dot2', subsequents=['dot3'], worker=PortListener('port')),
    Node('dot3', subsequents=['dot4', 'dot5'], worker=BWT901CL('b')),
    Node('dot4', worker=PrintData('print', [])),
    Node('dot5', worker=PoltData('Polt')),
])

task = NodeSet([
    dots1,
    dots2
])


if __name__ == '__main__':
    # dots1.run(Frame(end='head1'))
    MulIgnition([dots1, dots2]).run()

