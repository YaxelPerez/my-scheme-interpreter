#!/usr/bin/env python

from collections import ChainMap
from functools import reduce
import operator
import sys

import scheme
from lisptypes import (
    Expression,
    Symbol,
    String,
    Number,
    Integer,
    Float,
    List,
    Pair,
    Procedure,
    BuiltinProcedure
)
import lispbuiltins as builtins

def _bool(val):
    return Symbol('#t') if val else Symbol('#f')

def _builtin(f):
    def wrapper(env, *args):
        vals = [scheme.eval(arg, env) for arg in args]
        return f(env, *vals)
    return BuiltinProcedure(wrapper)

def _is(a, b):
    if type(a) == Symbol and type(b) == Symbol:
        return str(a) == str(b)
    else:
        return a is b

if __name__ == '__main__':
    env = ChainMap({
        # fundamentals
        'begin': BuiltinProcedure(builtins.begin),
        'define': BuiltinProcedure(builtins.define),
        'quote': BuiltinProcedure(builtins.quote),
        'if': BuiltinProcedure(builtins._if),
        'set!': BuiltinProcedure(builtins._set),
        'lambda': BuiltinProcedure(builtins._lambda),
        # equivalency
        'eq?': _builtin(lambda env, a, b: _bool(_is(a, b))),
        'eqv?': _builtin(builtins.eqv),
        'equal?': _builtin(builtins.equal),
        # logical operators
        'and': _builtin(builtins._and),
        'or': _builtin(builtins._or),
        'not': _builtin(lambda env, val: _bool(not val or val == Symbol('#f'))),
        # math
        '+': _builtin(lambda env, *args: Number(reduce(operator.add, args[1:], args[0]))),
        '-': _builtin(lambda env, *args: Number(reduce(operator.sub, args[1:], args[0]))),
        '*': _builtin(lambda env, *args: Number(reduce(operator.mul, args[1:], args[0]))),
        '/': _builtin(lambda env, *args: Number(reduce(operator.truediv, args[1:], args[0]))),
        'pow': _builtin(lambda env, a, b: Number(a ** b)),
        'mod': _builtin(lambda env, a, b: Number(a % b)),
        '=': _builtin(lambda env, *args: _bool(reduce(operator.eq, args[1:], args[0]))),
        '<': _builtin(lambda env, *args: _bool(reduce(operator.lt, args[1:], args[0]))),
        '>': _builtin(lambda env, *args: _bool(reduce(operator.gt, args[1:], args[0]))),
        '<=': _builtin(lambda env, *args: _bool(reduce(operator.le, args[1:], args[0]))),
        '>=': _builtin(lambda env, *args: _bool(reduce(operator.ge, args[1:], args[0]))),
        # list operations
        'list': _builtin(lambda env, *args: List(args)),
        'length': _builtin(lambda env, l: len(l)),
        'cons': _builtin(lambda env, a, b: Pair(a, b)),
        'car': _builtin(builtins.car),
        'cdr': _builtin(builtins.cdr),
        'null?': _builtin(lambda env, l: _bool(len(l) == 0)),
        'pair?': _builtin(builtins.pair),
        # system
        'exit': BuiltinProcedure(lambda env: sys.exit())
    })
    scheme.repl(env)
