# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402,W0718,W0212,W0613


"handler"


import inspect
import queue
import threading
import _thread


from .brokers import Broker
from .errored import Errors
from .message import Event
from .objects import Object
from .threads import launch



def __dir__():
    return (
            'Client',
            'Handler',
            'command'
           )


class Handler(Object):

    cmds = {}

    def __init__(self):
        Object.__init__(self)
        self.cbs = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.end = threading.Event()

    @staticmethod
    def add(func):
        Handler.cmds[func.__name__] = func

    def event(self, txt):
        evt = Event()
        evt.txt = txt
        evt.orig = object.__repr__(self)
        return evt

    def forever(self):
        self.stopped.wait()

    def dispatch(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        evt._thr = launch(func, evt)

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                self.dispatch(self.poll())
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self) -> Event:
        return self.queue.get()

    def put(self, evt):
        self.queue.put_nowait(evt)

    @staticmethod
    def scan(mod) -> None:
        for key, cmd in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Handler.add(cmd)

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)
        Broker.add(self)

    def announce(self, txt):
        self.raw(txt)

    def dosay(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        pass


def command(evt):
    func = Handler.cmds.get(evt.cmd, None)
    if not func:
        evt.ready()
        return
    try:
        func(evt)
        evt.show()
    except Exception as ex:
        exc = ex.with_traceback(ex.__traceback__)
        Errors.errors.append(exc)
    evt.ready()
