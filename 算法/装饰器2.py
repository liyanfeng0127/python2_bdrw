#-*-coding:utf8-*-

import sys
import functools

reload(sys)
sys.setdefaultencoding('utf-8')

def requires_ints(decorated):
    @functools.wraps(decorated)
    def inner(*args, **kwargs):
        kwarg_values = [i for i in kwargs.values()]

        for arg in list(args) + kwarg_values:
            if not isinstance(arg, int):
                raise TypeError('%s only accept integers as arguments.' % decorated.__name__)
        return decorated(*args, **kwargs)
    return inner

@requires_ints
def foo(x, y):
    """ Return the sum of x and y."""
    return x + y

# a = foo(3, 5)
# print a
help(foo)