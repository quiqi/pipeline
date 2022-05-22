# 这是一个连接工具包
import time
import serial
import cv2
import numpy as np

from base.model import Worker, Frame


class PortListener(Worker):
    """
    串口连接工具
    """
    def __init__(self, name, port: str = 'com11', baud_rate: int = 115200, timeout: float = 1, read_size: int = 33,
                 interval: float = 1):
        super().__init__(name)
        self.ser = None
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.off_line = 0
        self.read_size = read_size
        self.interval = interval
        self.last_time = time.time() + self.interval    # 第一次连接时默认不等待时间间隔

    def first_process(self, frame: Frame):
        try:
            if time.time() - self.last_time < self.interval:    # 每秒连接一次
                return False
            else:
                self.last_time = time.time()    # 重置链接时间
                self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)   # 尝试连接
                print('串口：{}启动成功!'.format(self.port))   # 连接成功
                self.off_line = 0   # 将self.off_line置为零
                return True
        except serial.SerialException:
            print('串口：{}启动失败，请检测设备开关是否打开，{}模块暂时关闭'.format(self.port, self.name))
            self.switch = False
            self.ser = None
            self.first = True
            time.sleep(1)
            return False

    def process(self, frame: Frame):
        data = self.ser.read(self.read_size)
        if len(data) < self.read_size:
            self.off_line += 1
            if self.off_line > 10:
                self.ser.close()
                self.first = True
        frame.data[self.port] = data
        # print('listener:{}'.format(frame))
        return frame

    def __del__(self):
        self.ser.close()


class WebCamera(Worker):
    def __init__(self, name, url: str, interval: float = 1):
        super().__init__(name)
        self.url = url
        self.camera = None
        self.interval = interval
        self.last_time = time.time() + self.interval

    def first_process(self, frame: Frame):
        try:        # 尝试连接摄像头
            if time.time() - self.last_time < self.interval:
                return False
            print('Try to connect the camera...')
            self.camera = cv2.VideoCapture(self.url)
            if not self.camera.isOpened():
                self.camera.release()
                return False    # 如果该摄像头没打开，表示连接失败
            else:
                print('connect the camera succeed!')
                return True     # 否则连接成功
        except Exception as e:  # 异常处理
            print(e)            # 打印异常信息
            return False        # 返回连接失败

    def process(self, frame: Frame):
        ret, img = self.camera.read()
        frame.data['img'] = img
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        cv2.imshow('img:{}'.format(self.name), img)
        cv2.waitKey(1)
        return frame


if __name__ == '__main__':
    from base.model import Dot, DotSet
    from base.utils import Source, PrintData, Save, PoltData
    from base.muldot import Mulignition
    from sensor.sensors import get_web_camera_input
    from pars_tools import BWT901CL
    wc1 = Dot('dot1', worker=get_web_camera_input('a'), source='dot1')    # 卧室
    wc2 = Dot('dot2', worker=WebCamera('web_camera2', 'rtsp://admin:a1234567@192.168.111.8:554/stream1'), source='dot2')    # 客厅
    wc3 = Dot('dot3', worker=WebCamera('web_camera3', 'rtsp://admin:a1234567@192.168.111.6:554/stream1'), source='dot3')    # 教室
    Mulignition([wc1, wc2, wc3]).run()

    # task = DotSet(dots=[
    #     Dot('head', subsequents=['bwt901cl_listener'], worker=Source()),
    #     Dot(worker=PortListener('bwt901cl_listener', port='com11'), subsequents=['bwt', 'save'], send_mod='copy'),
    #     Dot(worker=BWT901CL('bwt'), subsequents=['print']),
    #     # Dot(worker=PrintData('print', ['bwt901cl_listener_data'])),
    #     # Dot(worker=Save('save'))
    # ])
    #
    # for i in range(100):
    #     frame = Frame(end='head')
    #     task.run(frame)
