import multiprocessing
import typing

import base.model as model
import base.utils
import base.utils as utils

import numpy as np


class MulSource(base.utils.Source):
    def __init__(self):
        super().__init__(name='_MulSource')

    def after_process(self, frame: base.model.Frame):
        """
        用于阻塞进程
        :param frame:
        :return:
        """
        return frame


class Mulignition:
    def __init__(self, dots: typing.List[model.Dot], queue_size: int = 10):
        if len(dots) == 0:
            raise Exception('Please include at least one dot in dots')

        self.pipes = {}
        self.process_list = {}
        self.source = []

        # 初始化管道
        for dot in dots:
            if dot.name == '_SOURCE':  # dot 不可以以 '_SOURCE' 命名
                raise Exception('The dot can not named as "_SOURCE"! Please changing the name.')
            if dot.name not in self.pipes.keys():
                self.pipes[dot.name] = multiprocessing.Queue(queue_size)  # 为当前进程建立管道

                # 如果该进程为源头进程
                if dot.source is not None:  # 如果该dot是源头dot，则
                    if dot.source == dot.name:  # 如果dot名和起始节点同名，则将节点名加入 source 列表中
                        self.source.append(dot.name)
                    else:  # 否则将多级路径加入 source 列表中
                        self.source.append('{}/{}'.format(dot.name, dot.source))
            else:
                raise Exception('Two processes with the same name appear: {}.'
                                'Processes cannot have the same name'.format(dot.name))
        if len(self.source) == 0:
            self.source.append(dots[0].name)
        # 加入源头进程，一切的数据包都来源于源头进程
        source_dot = model.Dot('_SOURCE', subsequents=self.source, worker=MulSource())
        p = Mulignition.MulDot(source_dot, self.pipes)
        p.start()
        self.process_list['_SOURCE'] = p

        # 初始化进程
        for dot in dots:
            p = Mulignition.MulDot(dot, self.pipes)
            p.start()
            self.process_list[dot.name] = p  # 为当前进程创造进程对象

    def run(self):
        for process in self.process_list:
            self.process_list[process].join()

    class MulDot(multiprocessing.Process):
        def __init__(self, dot: model.Dot, pipes: dict):
            super(Mulignition.MulDot, self).__init__(name=dot.name)
            self.dot = dot
            self.pipes = pipes

        def run(self):
            if self.dot.name == '_SOURCE':  # 如果是源头节点，则自己生成数据
                while self.dot.switch:
                    frames = self.dot.run(model.Frame(end='_SOURCE'))
                    # print('s:{}'.format(frames[0].end))
                    for frame in frames:
                        if frame.end in self.pipes.keys():  # 安全检查，检查frame当前帧的目的地是否有对应的管道
                            self.pipes[frame.end].put(frame)  # 如果有，则将当前帧放入管道中
                        else:
                            pass  # 否则什么也不干，相当于抛弃这个帧
            else:
                while self.dot.switch:  # 如果是非源头节点，则直接从自己的管道中读取数据
                    frame = self.pipes[self.dot.name].get()
                    if frame is not None:
                        frames = self.dot.run(frame)
                        # print('d:{} run, data:{}'.format(self.dot.name, frames[0].data))
                        for frame in frames:  # 按地址发送每一个帧
                            if frame.end in self.pipes.keys():  # 安全检查，检查frame当前帧的目的地是否有对应的管道
                                self.pipes[frame.end].put(frame)  # 如果有，则将当前帧放入管道中
                            else:
                                pass  # 否则什么也不干，相当于抛弃这个帧
