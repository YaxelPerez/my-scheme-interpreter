#!/usr/bin/env python

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


def quote(env, val):
    return val


def _if(env, predicate, if_expr, else_expr):
    if scheme.eval(predicate, env) == Symbol('#t'):
        return scheme.eval(if_expr, env)
    else:
        return scheme.eval(else_expr, env)


def begin(env, *args):
    last = List()
    for expr in args:
        last = scheme.eval(expr, env)
    return last


def define(env, id, *body):
    if type(id) == List:
        # procedure definition
        head, *args = id
        env[str(head)] = Procedure(args, body)
        return List()
    else:
        assert len(body) > 0, "Expression required for assignment."
        assert len(body) < 2, "Cannot assign multiple values to single identifier."
        env[str(id)] = scheme.eval(body[0], env)
        return List()


def _lambda(env, args, *body):
    return Procedure(args, body)


def car(env, val):
    if type(val) == Pair:
        return val.car
    else:
        return val[0]

def cdr(env, val):
    if type(val) == Pair:
        return val.cdr
    else:
        return List(val[1:])


def pair(env, val):
    if type(val) == Pair:
        return Symbol('#t')
    else:
        return Symbol('#t') if len(val) > 0 else Symbol('#f')


def _set(env, id, val):
    env[str(id)] = scheme.eval(val, env)
    return List()


def eqv(env, a, b):
    if type(a) != type(b):
        return Symbol('#f')
    return Symbol('#t') if a == b else Symbol('#f')


def equal(env, a, b): # recursive comparison
    if type(a) != List or type(b) != List:
        return Symbol('#t') if a == b else Symbol('#f')
    else:
        if len(a) != len(b):
            return Symbol('#f')
        for i in range(len(a)):
            if not equal(env, a[i], b[i]):
                return Symbol('#f')
        return Symbol('#t')


def _and(env, *args):
    for arg in args:
        if not arg or arg == Symbol('#f'):
            return Symbol('#f')
    return Symbol('#t')


def _or(env, *args):
    for arg in args:
        if arg or arg == Symbol('#t'):
            return Symbol('#t')
    return Symbol('#f')
