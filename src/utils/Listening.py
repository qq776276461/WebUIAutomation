import threading
from time import sleep


class Listening:

    def __init__(self, func, log, interval=2.0):
        self.__log = log
        self.__func = func
        self.__interval = interval
        self.__lock = threading.Lock()
        self.__stop = threading.Event()
        self.__stopped = threading.Event()
        self.__started = False

    def _run_func(self):
        try:
            while not self.__stop.is_set():
                with self.__lock:
                    try:
                        if self.__func():
                            return
                    except Exception as e:
                        self.__log.exception(e)
                sleep(self.__interval)
        finally:
            self.__stopped.set()

    def start(self):
        if not self.__func:
            return
        if self.__started:
            return
        self.__log.debug(f'启动线程: {self.__func}')
        self.__started = True
        self.__stop.clear()
        self.__stopped.clear()
        threading.Thread(target=self._run_func, daemon=True).start()

    def stop(self):
        if not self.__func:
            return
        self.__stop.set()
        self.__stopped.wait(self.__interval)
        self.__started = False
        self.__log.debug(f'停止线程: {self.__func}')
