import random
import copy
import collections


class Frame:
    """
    帧类，数据流动的基本单位
    """
    def __init__(self, start=None, end=None, lifetime: int = 100, cycle: bool = False):
        self.data = {}      # 数据字典：组件之间的数据交流载体
        self.info = {}      # 信息列表：为基础组件预留的接口，用户一般不要使用，以免发生错误
        self.ctrl = []      # 控制列表：控制数据，用于系统控制和人机交互
        self.visited = []   # 经过节点：该帧经过的节点的名称
        self.start = start  # 最后发出该帧的节点
        self.end = end      # 该帧目前的目标节点
        self.itinerary = collections.deque()    # 行程计划
        self.lifetime = lifetime
        self.cycle = cycle

    def send(self, start, end):       # send函数，用于设置该帧的流向
        if end is not None and '/' in end:      # 如果end包含分隔符，则认为这是一个路径，一般用于设置跨DotSet的跳转
            ends = end.split('/')
            for e in ends:
                self.itinerary.append(e)
        if not self.cycle:
            self.visited.append(start)  # 对于非循环帧，将起点放入访问过的节点
        self.start = start
        self.end = end
        if len(self.itinerary) == 0:  # 如果当前没有行程安排，按end参数流动
            self.end = end
        else:
            self.end = self.itinerary.popleft()     # 否则按行程安排流动

        # 消除死循环帧
        if not self.cycle:      # 对于非循环帧，每次运行都减少帧的寿命
            self.lifetime -= 1
            if self.lifetime <= 0:  # 当寿命减到0则将后继节点设为 None，强制帧退出程序
                self.end = None


class Model:
    """
    Worker 和 Dot 的父类，暂时什么用也没有，仅为后续可能的拓展留下余地
    """
    def __init__(self, name):
        self.name = name    # model的名字
        self.switch = True
        pass
    
    def process(self, frame: Frame):
        return frame

    def run(self, frame: Frame):
        """
        在 Worker 和 Dot 中重写，该函数重来没有被运行
        :param frame:
        :return:
        """
        return frame


class Worker(Model):
    """
    所有组件的基类，具体功能实现的承担者。
    """
    def __init__(self, name):
        super().__init__(name)
        print('worker:{} staring...'.format(self.name))
        self.switch = True      # 组件开关，当self.switch = False 时，组件功能关闭
        self.first = True       # 表示组件是否是第一次运行，当第一运行开始时，将会被设置为 False，但用户可以在first_process中重新设置为True

    def first_process(self, frame: Frame):
        """
        当组件第一次运行时被调用，一般用于运行时的准备工作，比如网络连接、设备连接、文件夹创建等
        :param frame: 帧数据
        :return: 修改后的帧数据
        """
        return frame
        pass

    def pre_process(self, frame: Frame):
        """
        在process运行之前被调用，一般用做转接器且一般不在功能worker中实现，而在临时worker中实现。
        :param frame: 帧数据
        :return: 修改后的帧数据
        """
        return frame

    def after_process(self, frame: Frame):
        """
        在process运行之后被调用，一般用做转接器且一般不在功能worker中实现，而在临时worker中实现
        :param frame: 帧数据
        :return: 修改后的数据
        """
        return frame

    def process(self, frame: Frame):
        """
        承担功能实现的具体函数，一般在功能worker中被实现
        :param frame:帧数据
        :return:修改后的数据
        """
        return frame

    def run(self, frame: Frame):
        """
        运行函数，被Dot调用
        :param frame: 帧数据
        :return: 修改后的帧数据
        """
        if self.first:  # 如果时第一次运行
            self.first = False      # 将 self.first 设为 False
            print('worker:{} has been invoked.'.format(self.name))
            frame = self.first_process(frame)   # 运行 first_process，在用户重写时，可以将 self.first 重新设为 True
        if not self.switch:     # 如果组件开关关闭，则直接返回 传入的 frame
            return frame

        frame = self.pre_process(frame)     # 前处理调用
        frame = self.process(frame)         # 处理调用
        frame = self.after_process(frame)   # 后处理调用
        return frame    # 返回处理后的帧


class WorkerSet(Worker):
    """
    用于完成worker的线性合作
    """
    def __int__(self, workers: list):
        ex = Exception('elements in workers have to the type of Worker!')
        for work in workers:    # 检查传入的 list中的每一个元素是否都是一个 worker 类的对象
            if not isinstance(work, Worker):
                raise ex
        self.workers = workers

    def process(self, frame: Frame):
        """
        WorkerSet的process会依次调用workers中的组件，并返回最终结果
        :param frame: 帧序列
        :return: 处理后的帧序列
        """
        for worker in self.workers:     # 依次调用 workers 中组件的run
            frame = self.run(frame)
        return frame


class Dot(Model):
    """
    用于完成worker的网状合作
    """
    def __init__(self, name: str = None,  subsequents: list = None, worker: Worker = None, send_mod: str = None, source: str = None):
        """
        Dot的初始化函数
        :param name: Dot对象的名字，在同一个DotSet中，Dot的名字必须互异
        :param subsequents: 后记节点列表，优先在同一个DotSet中寻找。
        :param worker: 该类需要实现的功能
        :param send_mod: 当有多个后继时规定发送模式
        :param source: 源头节点的名字
        """
        super().__init__(name)
        if subsequents is None:     # 若没有指定后继节点，默认后继节点为空
            subsequents = []

        if type(subsequents) is str:    # 若只有一个后继节点，将被包装为一个长度为1的list
            subsequents = [subsequents]

        self.worker = worker        # 指定Dot的工作
        if worker is not None and self.name is None:    # 当Dot被指定工作且没有被指定名称时，用worker的名称作为Dot的名称
            self.name = worker.name
        if send_mod is None:    # 当有多个后继时，默认的发送模式为复制发送
            send_mod = 'copy'
        self.subsequents = subsequents      # 后继节点
        self.send_mod = send_mod            # 发送模式
        if len(self.subsequents) == 1:      # 如果只有一个后继节点，发送模式被设置为只向第一个后继发送帧数据
            self.send_mod = 'first'

        if source is not None:
            self.source = name
        else:
            self.source = None

    def process(self, frame: Frame):
        if self.worker is not None:     # 如果Dot被指定工作，则执行worker的run
            try:
                worker_frame = self.worker.run(frame)
                self.worker.switch = True
            except Exception as e:      # 捕获worker的错误，增强代码的健壮性
                print(e)                # 打印错误
                print('function named "run" of module:{}. '     # 输出提示
                      'Check your code in functions of process, pre_process and after_process, '
                      'and this module was temporarily disabled'.format(self.worker.name))
                self.worker.switch = False  # 当出现错误时关闭worker
                worker_frame = frame        # 相当传回未被修改的帧

            if worker_frame is None:        # 如果worker返回的是空数据，打印提示信息
                print('function named "run" of module:{} return None.'
                      'This may be caused by function of process'
                      '(pre_process/after_process/first_process) forgetting to write a return, '
                      'please check your code, the module is temporarily closed.'.format(self.worker.name))
                self.worker.switch = False
            else:
                frame = worker_frame        # 将frame赋值为worker_frame继续执行

        if len(self.subsequents) != 0:      # 如果有后继节点，则调用send函数发送
            frames = self.send(frame)
            return frames
        else:                               # 如果没有后继节点，则将frame的end置None，并变成list返回
            frame.send(self.name, None)
            frames = [frame]
            return frames
    
    def run(self, frame: Frame):
        if self.switch:
            return self.process(frame)
        else:
            return [frame]
    
    def send(self, frame: Frame):
        frames = []     # 待发送的帧
        if self.send_mod == 'first':        # 如果 发送模式为 first 则只为第一个后继发送数据
            frame.send(self.name, self.subsequents[0])
            frames.append(frame)
        elif self.send_mod == 'random':     # 随机发送给任意一个节点
            r = random.choice(self.subsequents)
            frame.send(self.name, r)
        elif self.send_mod == 'copy':       # 为每一个节点发送一个副本
            for subsequent in self.subsequents:
                c_frame = copy.deepcopy(frame)
                c_frame.send(self.name, subsequent)
                frames.append(c_frame)
        return frames


class DotSet(Dot):
    """
    Dot的子类，Dot列表（也就是一张图）的容器和启动器，也可以当作Dot放入另一个DotSet套娃。
    """
    def __init__(self, dots: list, subsequents: list = None, source: str = None):
        """
        Dot的初始化函数
        :param dots: 一个 Dot列表，列表中的Dot对象不能重名
        :param subsequents: 后继节点
        """
        super().__init__(dots[0].name, subsequents)
        self.dots = {}
        ex1 = Exception('elements in workers have to the Worker!')
        ex2 = Exception('can not have two dot with the same name!')
        for dot in dots:
            if not isinstance(dot, Dot):        # 检查dots中的每一个元素是否都是Dot类的对象
                raise ex1
            if dot.name in self.dots.keys():    # 检查是否有重名的 Dot 对象
                raise ex2
            self.dots[dot.name] = dot           # 将dot字典化，加快查找速度

        # 如果source不为空
        if source is not None:
            if source in self.dots.keys():
                self.source = source
            else:
                self.source = self.name
        else:
            self.source = None

    def process(self, frame: Frame):
        """
        运行DotSet中的Dot节点，主要功能是管理帧在DotSet内部的传递
        :param frame: 传入的帧
        :return: 生成的帧组（一个Frame的list）
        """
        t_frames = collections.deque()      # 待处理的帧
        finish = []                         # 处理完毕的帧
        t_frames.append(frame)              # 将传入帧放入队列
        while not len(t_frames) == 0:       # 若帧队列中还有待处理的帧
            frame = t_frames.popleft()      # 取出一个待处理的帧

            # 控制信息处理
            for c in frame.ctrl:
                if c == '_CLOSE':   # 如果在控制信息中出现 _CLOSE 就关闭当前 DotSet，但仍会执行完下面的部分
                    self.switch = False   
            
            # 如果当前需要发送的节点没有在DotSet中，则将该节点放入 finish中
            if frame.end not in self.dots.keys():
                finish.append(frame)
                continue
                
            # 将当前帧放入指定节点中运行
            frames = self.dots[frame.end].run(frame)
            for frame in frames:    # 对得到的帧进行处理
                if frame is None:   # 过滤掉None（一般不会出现None）
                    continue
                if frame.end is None:   # 如果帧的尾地址为空，则认为该帧处理结束，加入finish
                    finish.append(frame)
                else:                   # 否则加入 t_frames 继续处理
                    t_frames.append(frame)
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




