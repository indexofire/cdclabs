# -*- coding: utf-8 -*-
# code from http://code.activestate.com/recipes/586965/
import threading


class Executor(object):
    """
    Base class for execute the emboss's apps
    """
    def __init__(self, generator, exec_handler=print_exec):
        """
        Create the executor

        `generator`:

        `exec_handler`:
        """
        self.__generator = generator
        self.__exec_handler = exec_handler
        self.__throw = generator.throw
        self.__send = generator.send
        self.__next = generator.next
        self.__close = generator.close

    def __iter__(self):
        return self

    def __call_gen(self, method, *args, **keys):
        """
        """
