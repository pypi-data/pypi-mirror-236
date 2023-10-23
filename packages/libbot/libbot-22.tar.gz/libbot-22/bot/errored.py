# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402,E1102,R0903,C0103


"errors"


import io
import sys
import traceback


from .objects import Object


def __dir__():
    return (
            'Censor',
            'Errors',
            'cprint',
            'debug',
            'output',
            'shutdown'
            )


output = None


class Censor(Object):

    words = []

    @staticmethod
    def skip(txt) -> bool:
        for skp in Censor.words:
            if skp in str(txt):
                return True
        return False


class Errors(Object):

    errors = []

    @staticmethod
    def format(exc):
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            res += line + "\n"
        return res

    @staticmethod
    def handle(exc):
        if output:
            output(Errors.format(exc))

    @staticmethod
    def show():
        for exc in Errors.errors:
            Errors.handle(exc)


def cprint(txt):
    if output is None:
        return
    if Censor.skip(txt):
        return
    output(txt)
    sys.stdout.flush()


def debug(txt):
    cprint(txt)


def shutdown():
    Errors.show()
