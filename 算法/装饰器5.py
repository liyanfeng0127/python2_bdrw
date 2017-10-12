#-*-coding:utf8-*-

import sys
import functools
import logging
import time


reload(sys)
sys.setdefaultencoding('utf-8')

def logged(method):
    @functools.wraps(method)
    def inner(*args, **kwargs):
        start = time.time()
        return_values = method(*args, **kwargs)

        end = time.time()
        delta = end - start

        logger = logging.getLogger('decorated.logged')
        logger.warn('Called method %s at %.02f; execution time %.02f' 
                    'seconds; result %r.' %
                    (method.__name__, start, delta, return_values))

        return return_values
    return inner

