#-*-coding:utf8-*-

import sys
import functools
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def json_output(decorated):
    @functools.wraps(decorated)
    def inner(*args, **kwargs):
        result = decorated(*args, **kwargs)
        return json.dumps(result)
    return inner

@json_output
def do_nothing():
    return {'status': 'done'}

print do_nothing