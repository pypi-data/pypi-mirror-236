import threading

def msgFormat(msg):
    # 将转义字符替换回特殊字符
    msg = msg.replace('&quot;', '"')
    msg = msg.replace('&amp;', '&')
    msg = msg.replace('&lt;', '<')
    msg = msg.replace('&gt;', '>')
    return msg

class StopableThread(threading.Thread):
    # def __init__(self) -> None:
    #     super(StopableThread,self).__init__()
    #     self.stop_event = threading.Event()
    def __init__(self, target , args , kwargs) -> None:
        super().__init__(target = target, args = args, kwargs = kwargs)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


def async_call(fn):
    def wrapper(*args, **kwargs):
        th = StopableThread(target=fn, args=args, kwargs=kwargs)
        th.setDaemon(True)
        th.start()
        return th.stop
    return wrapper