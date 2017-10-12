#-*-coding:utf8-*-

import sys
import functools

reload(sys)
sys.setdefaultencoding('utf-8')

class User(object):
    def __init__(self, username, email):
        self.username = username
        self.email = email

class AnonymousUser(User):
    def __init__(self):
        self.username = None
        self.email = None

    def __nonzero__(self):
        return  False

def requires_user(func):
    @functools.wraps(func)
    def inner(user, *args, **kwargs):
        if user and isinstance(user, User):
            return func(user, *args, **kwargs)
        else:
            raise ValueError('a VALID user ie required to run this .')
    return inner


