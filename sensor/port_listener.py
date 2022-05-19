import serial

from base.model import Worker, Frame


class PortListener(Worker):
    def __init__(self, name, port: str = 'com11', baud_rate: int = 115200, timeout: float = 1):
        super().__init__(name)
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=timeout)
            print('串口：{}启动成功!'.format(port))
        except serial.SerialException:
            print('串口：{}启动失败，请检测设备开关是否打开，{}模块暂时关闭'.format(port, self.name))
            self.switch = False
            self.ser = None
            # self.ser.timeout = 0.005

    def process(self, frame: Frame):
        data = self.ser.read(33)
        frame.data['{}_data'.format(self.name)] = data
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
