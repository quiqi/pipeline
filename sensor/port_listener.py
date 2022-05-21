import time

import serial

from base.model import Worker, Frame


class PortListener(Worker):
    def __init__(self, name, port: str = 'com11', baud_rate: int = 115200, timeout: float = 1):
        super().__init__(name)
        self.ser = None
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout

    def first_process(self, frame: Frame):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print('串口：{}启动成功!'.format(self.port))
        except serial.SerialException:
            print('串口：{}启动失败，请检测设备开关是否打开，{}模块暂时关闭'.format(self.port, self.name))
            self.switch = False
            self.ser = None
            self.first = True
            time.sleep(1)
            return frame
        return frame

    def process(self, frame: Frame):
        data = self.ser.read(33)
        frame.data['{}_data'.format(self.name)] = data
        # print('listener:{}'.format(frame))
        return frame


if __name__ == '__main__':
    from base.model import Dot, DotSet
    from base.utils import Source, PrintData, Save, PoltData
    from sensor_data_parsing import BWT901CL
    task = DotSet(dots=[
        Dot('head', subsequents=['bwt901cl_listener'], worker=Source()),
        Dot(worker=PortListener('bwt901cl_listener', port='com13'), subsequents=['bwt', 'save'], send_mod='copy'),
        Dot(worker=BWT901CL('bwt'), subsequents=['print']),
        # Dot(worker=PrintData('print', ['bwt901cl_listener_data'])),
        # Dot(worker=Save('save'))
    ])

    for i in range(100):
        frame = Frame(end='head')
        task.run(frame)
