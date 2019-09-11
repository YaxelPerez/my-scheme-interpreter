#!/usr/bin/env python
from decimal import Decimal as decimal


class Expression:
    pass

# Self-evaluating data types:

class String(str, Expression):
    def __repr__(self):
        return f"<String: '{str(self)}'>"


class Symbol(str, Expression):
    def __repr__(self):
        return f"<Symbol: '{str(self)}'>"

    def __eq__(self, other):
        return type(other) == Symbol and str(self) == str(other)


class Number(Expression):
    def __new__(cls, val):
        if type(val) == float:
            return Float(val)
        elif type(val) == int:
            return Integer(val)

    def __repr__(self):
        return f"<Number: {str(self)}>"


class Float(float, Number):
    pass


class Integer(int, Number):
    pass

# compound data types

class List(list, Expression):
    def __str__(self):
        if len(self) > 0:
            if type(self[0]) == Symbol and self[0] == 'quote':
                return f'\'{ str(self[1]) }'
            return f'({ " ".join(str(i) for i in self) })'
        else:
            return '()'

    def __repr__(self):
        return f'<List: {str(self)}>'


class Pair(Expression):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return f'<Pair: {repr(self.car)} . {repr(self.cdr)}>'


class Procedure(Expression):
    def __init__(self, arguments, body):
        self.arguments = arguments
        self.body = body


class BuiltinProcedure(Expression):
    def __init__(self, f):
        self.f = f

    def call(self, *args):
        return self.f(*args)
