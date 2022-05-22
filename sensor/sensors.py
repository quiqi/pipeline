from base.model import Worker, Frame
from sensor.pars_tools import BWT901CL
from sensor.connect_tools import PortListener, WebCamera


# 9轴传感器数据接口
class BWT901CLInput(Worker):
    def __init__(self, name: str = 'BWT901CLInput', port: str = 'cmd11'):
        super().__init__(name)
        self.pl = PortListener('bwt901cl_listener_{}'.format(port))
        self.dp = BWT901CL('bwt901cl_pars_{}'.format(port), port=port)

    def process(self, frame: Frame):
        frame = self.pl.run(frame)
        frame = self.dp.run(frame)
        return frame


def get_web_camera_input(name: str = 'classroom'):
    if name == 'classroom':
        url = 'rtsp://admin:a1234567@192.168.111.6:554/stream1'
    elif name == 'living_room':
        url = 'rtsp://admin:a1234567@192.168.111.8:554/stream1'
    elif name == 'bed_room':
        url = 'rtsp://admin:a1234567@192.168.111.9:554/stream1'
    else:
        print("can't find the {} camera,and the default call the camera in local".format(name))
        name = 'local'
        url = 0
    return WebCamera(name=name, url=url)
