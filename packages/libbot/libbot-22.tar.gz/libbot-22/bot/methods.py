# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402


"methods"


import datetime
import os
import uuid


from .objects import items, keys


def __dir__():
    return (
            'edit',
            'fmt',
            'fqn',
            'ident',
            'search'
           )


def edit(obj, setter, skip=False):
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            obj[key] = int(val)
            continue
        except ValueError:
            pass
        try:
            obj[key] = float(val)
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            obj[key] = True
        elif val in ["False", "false"]:
            obj[key] = False
        else:
            obj[key] = val


def fmt(obj, args=None, skip=None) -> str:
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in sorted(args):
        if key in skip:
            continue
        try:
            value = obj[key]
        except KeyError:
            continue
        if isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f'{key}={value} '
    return txt.strip()


def fqn(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def ident(obj) -> str:
    return os.path.join(
                        fqn(obj),
                        str(uuid.uuid4().hex),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def search(obj, selector) -> bool:
    res = False
    for key, value in items(selector):
        if key not in obj:
            res = False
            break
        val = obj[key]
        if str(value) in str(val):
            res = True
            break
    return res
