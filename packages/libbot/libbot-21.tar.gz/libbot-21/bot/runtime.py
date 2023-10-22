# This file is placed in the Public Domain.
#
# pylint: disable=C0412,C0115,C0116,W0212,R0903,C0207,C0413,W0611
# pylint: disable=C0411,E0402,E0611,C2801


"runtime"


import getpass
import importlib
import os
import pwd
import readline
import shutil
import sys
import termios
import time
import threading
import traceback


from .brokers import Broker
from .configs import Cfg, Config
from .errored import Errors, cprint, debug, shutdown
from .message import Event
from .handler import Client, Reactor, command
from .parsers import parse
from .scanner import scan
from .storage import Storage
from .threads import launch, name
from .utility import daemon, laps, mods, privileges, spl


from . import errored
from . import modules


errored.output = print


class CLI(Client):

    def announce(self, txt):
        pass

    def raw(self, txt):
        print(txt)
        sys.stdout.flush()


class Console(CLI):

    def dispatch(self, evt):
        parse(evt)
        command(evt)
        evt.wait()

    def poll(self) -> Event:
        return self.event(input("> "))


def wrap(func) -> None:
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
        sys.stdout.flush()
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def upt(event):
    event.reply(laps(time.time()-Cfg.starttime))


def ver(event):
    event.reply(f"{Cfg.name.upper()} {Cfg.version}")


def main():
    parse(Cfg, " ".join(sys.argv[1:]))
    Cfg.mod = ",".join(modules.__dir__())
    if "n" in Cfg.opts:
        Cfg.commands = False
    if "d" in Cfg.opts:
        daemon(Cfg.pidfile)
    if "d" in Cfg.opts or "s" in Cfg.opts:
        privileges(getpass.getuser())
        debug(f"dropped to {Cfg.user} privileges")
        scan(modules, Cfg.mod, True)
        while 1:
            time.sleep(1.0)
    elif "c" in Cfg.opts:
        dtime = time.ctime(time.time()).replace("  ", " ")
        if "v" in Cfg.opts:
            cprint(f"{Cfg.name.upper()} started at {dtime} {Cfg.opts.upper()} {Cfg.mod.upper()}")
        thrs = scan(modules, Cfg.mod, "x" not in Cfg.opts)
        if "w" in Cfg.opts:
            for thr in thrs:
                thr.join()
                cprint(f"ready {thr.name}")
        csl = Console()
        csl.add(ver)
        csl.add(upt)
        csl.start()
        csl.forever()
    else:
        cli = CLI()
        cli.add(ver)
        scan(modules, Cfg.mod)
        evt = cli.event(Cfg.otxt)
        parse(evt)
        command(evt)
        evt.wait()


if __name__ == "__main__":
    wrap(main)
    shutdown()
