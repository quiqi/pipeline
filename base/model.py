import random
import copy
import queue


class Frame:
    def __init__(self, start=None, end=None):
        self.data = {}      # 数据字典：
        self.info = {}      # 信息列表
        self.ctrl = []      # 控制列表
        self.visited = []   # 经过节点
        self.start = start
        self.end = end

    def send(self, start, end):
        self.visited.append(start)
        self.start = start
        self.end = end


class Model:
    def __init__(self, name):
        self.name = name
        pass

    def process(self, frame: Frame):
        return frame
        pass

    def run(self, frame: Frame):
        return self.process(frame)
        pass


class Worker(Model):
    def __init__(self, name):
        super().__init__(name)
        print('{}组件启动中'.format(self.name))
        self.switch = True
        self.first = True

    def pre_process(self, frame: Frame):
        return frame

    def after_process(self, frame: Frame):
        return frame

    def process(self, frame: Frame):
        return frame

    def run(self, frame: Frame):
        if self.first:
            print('{}组件被调用'.format(self.name))
            self.first = False
        if not self.switch:
            return frame

        frame = self.pre_process(frame)
        frame = self.process(frame)
        frame = self.after_process(frame)
        return frame


class WorkerSet(Worker):
    """
    用于完成worker的线性合作
    """
    def __int__(self, workers: list):
        ex = Exception('elements in workers have to the Worker!')
        for work in workers:
            if not isinstance(work, Worker):
                raise ex
        self.workers = workers

    def process(self, frame: Frame):
        for worker in self.workers:
            frame = self.run(frame)
        return frame


class Dot(Model):
    """
    用于完成worker的网状合作
    """
    def __init__(self, name: str = None,  subsequents: list = None, worker: Worker = None, send_mod: str = None):
        super().__init__(name)
        if subsequents is None:
            subsequents = []

        if type(subsequents) is str:
            subsequents = [subsequents]
        self.worker = worker
        if worker is not None and self.name is None:
            self.name = worker.name
        if send_mod is None:
            send_mod = 'copy'
        self.subsequents = subsequents
        self.send_mod = send_mod
        if len(self.subsequents) == 1:
            self.send_mod = 'first'

    def run(self, frame: Frame):
        if self.worker is not None:
            frame = self.worker.run(frame)

        if len(self.subsequents) != 0:
            frames = self.send(frame)
            return frames
        else:
            frame.send(self.name, None)
            frames = [frame]
            return frames

    def send(self, frame: Frame):
        frames = []
        if self.send_mod == 'first':
            frame.send(self.name, self.subsequents[0])
            frames.append(frame)
        elif self.send_mod == 'random':
            r = random.choice(self.subsequents)
            frame.send(self.name, r)
        elif self.send_mod == 'copy':
            for subsequent in self.subsequents:
                c_frame = copy.deepcopy(frame)
                c_frame.send(self.name, subsequent)
                frames.append(c_frame)
        return frames


class DotSet(Dot):
    def __init__(self, dots: list, subsequents: list = None):
        super().__init__(dots[0].name, subsequents)
        self.dots = {}
        self.switch = True
        ex1 = Exception('elements in workers have to the Worker!')
        ex2 = Exception('can not have two dot with the same name!')
        for dot in dots:
            if not isinstance(dot, Dot):
                raise ex1
            if dot.name in self.dots.keys():
                raise ex2
            self.dots[dot.name] = dot

    def run(self, frame: Frame):
        t_frames = queue.Queue()
        finish = []
        t_frames.put(frame)
        while not t_frames.empty():
            frame = t_frames.get()
            if '_CLOSE' in frame.ctrl:
                self.switch = False
            if frame.end not in self.dots.keys():
                finish.append(frame)
                continue
            frames = self.dots[frame.end].run(frame)
            for i in frames:
                if i is None:
                    pass
                if i.end is None:
                    finish.append(i)
                else:
                    t_frames.put(i)
        return finish


if __name__ == '__main__':
    dots = [
        Dot('dot0', ['dot1', 'dot2', 'dot3'], send_mod='copy'),
        Dot('dot1', ['dot2']),
        Dot('dot2')
    ]
    dots2 = [
        DotSet(dots),
        Dot('dot3', )
    ]
    for i in range(100):
        DotSet(dots2).run(Frame(None, 'dot0'))




