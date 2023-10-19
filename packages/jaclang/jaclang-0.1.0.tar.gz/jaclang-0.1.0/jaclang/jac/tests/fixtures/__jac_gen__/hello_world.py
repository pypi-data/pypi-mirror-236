""" Basic Hello World function """  # 0 1
from __future__ import annotations
import traceback as __jac_traceback__  # -1 0
from jaclang import handle_jac_error as __jac_error__  # -1 0
def hello():  # 0 3
    try:      # 0 3
        return "Hello World!"  # 0 4
    except Exception as e:      # 0 3
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 3
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 3
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 3
        raise e          # 0 3

r""" JAC DEBUG INFO
/home/ninja/jaclang/jaclang/jac/tests/fixtures/hello_world.jac
JAC DEBUG INFO """