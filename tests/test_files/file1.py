import module1

from module2 import module3

from .file2 import module4


def module8(string):
    pass


def module5():
    module3()
    module1()
    module4()
    module8('string1')


def module9():
    pass
