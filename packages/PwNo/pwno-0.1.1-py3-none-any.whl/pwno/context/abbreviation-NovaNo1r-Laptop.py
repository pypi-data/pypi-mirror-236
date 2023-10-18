import inspect

from typing import TypeVar, Callable, Any
from pwn import *

T = TypeVar('T', bound=Callable[..., Any])
def abbr(func: T) -> T:
    """
    提供一个函数的缩写，默认提供了以下缩写：
        send = process.send
        sl = process.sendline
        sa = process.sendafter
        sla = process.sendlineafter

        recv = process.recv
        recvu = process.recvuntil
        recvn = process.recvn
        recvl = process.recvline

        interactive = process.interactive
    """
    f = func.__name__
    if inspect.ismethod(func):
        for k, v in reversed(inspect.currentframe().f_back.f_locals.items()):
            if v == func.__self__:
                name = k
                break
    else:
        name = ''

    def get_instance(force=False):
        nonlocal name
        ctx = inspect.currentframe().f_back.f_back.f_locals
        if name == '' or force:
            for k, v in reversed(ctx.items()):
                if isinstance(v, (pwnlib.tubes.process.process, pwnlib.tubes.remote.remote)):
                    name = k
                    break
        return ctx[name]
    
    def inner(*args, **kwargs):
        sh = get_instance()
        if sh.poll() is not None:
            sh = get_instance(True)
        return getattr(sh, f)(*args, **kwargs)
    return inner

sl = abbr(process.sendline)
recv = abbr(process.recv)