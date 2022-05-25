from base.model import *
from base.utils import *

if __name__ == '__main__':
    dots = DotSet([
        Dot('dot1', worker=Load(load_path='./output/data-acquisition_1_set3/com14/'), subsequents=['dot2']),
        Dot('dot2', worker=PoltData('plot'))
    ])
    while dots.switch:
        dots.run(Frame(end='dot1'))
