#!/usr/bin/env python
# encoding: utf-8


class Event(object):
    def __init__(self):
        self.__handlers = set()

    def __iadd__(self, handler):
        self.__handlers.add(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.discard(handler)
        return self

    def fire(self, *args, **kwargs):
        for handler in self.__handlers:
            handler(*args, **kwargs)

    def clear(self):
        self.__init__()

    def clear_obj_handler(self, obj):
        self.__handlers = [h for h in self.__handlers if h.__self__ != obj]


def tick_to_dict(i):
    return to_dict(i)


def bar_to_dict(i):
    return to_dict(i)


def dailybar_to_dict(i):
    return to_dict(i)


def order_to_dict(i):
    return to_dict(i)


def execrpt_to_dict(i):
    return to_dict(i)


def cash_to_dict(i):
    return to_dict(i)


def position_to_dict(i):
    return to_dict(i)


def indicator_to_dict(i):
    return to_dict(i)

def instrument_to_dict(i):
    return to_dict(i)


def constituent_to_dict(i):
    return to_dict(i)


def broker_account_to_dict(i):
    return to_dict(i)


def to_dict(i):
    keys = [k for k in dir(i) if not k.startswith('__')]
    return dict(zip(keys, [i.__getattribute__(k) for k in keys]))
