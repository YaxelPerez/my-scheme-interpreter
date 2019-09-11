#!/usr/bin/env python
from lark import Lark, Transformer
from lark.exceptions import ParseError, UnexpectedCharacters

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from prompt_toolkit.lexers import PygmentsLexer

from pygments.lexers.lisp import SchemeLexer
from pygments.styles import get_style_by_name

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

parser = Lark(r"""

values: value*

?value: list
      | quote
      | float
      | integer
      | string
      | symbol

list: "(" [value value*] ")" | "[" [value value*] "]"
quote: "'" value

float: SIGNED_FLOAT
integer: SIGNED_INT

string: ESCAPED_STRING
symbol: SYMBOL

SYMBOL: /[A-Za-z!$,_\-.\/:;?+<=>#%&*@\\|`^~][A-Za-z0-9!$,_\-.\/:;?+<=>#%&*@\\|`^~]*/

COMMENT: /;[^\n]*/

%import common.WS
%import common.SIGNED_FLOAT
%import common.SIGNED_INT
%import common.ESCAPED_STRING

%ignore WS
%ignore COMMENT

""", start='values')


class SchemeTransformer(Transformer):
    def list(self, items):
        return List(items)

    def quote(self, items):
        return List([Symbol('quote')] + items)

    def symbol(self, items):
        return Symbol(items[0])

    def string(self, items):
        return String(bytes(items[0][1:-1], 'utf8').decode('unicode_escape'))

    def integer(self, items):
        return Integer(items[0])

    def float(self, items):
        return Float(items[0])

    def values(self, items):
        return items

transformer = SchemeTransformer()


def read_exprs(session, env):
    completer = WordCompleter((word for word in env.keys()))
    expr_str = ''
    prompt = '> '
    while True:
        try:
            expr_str += session.prompt(prompt, completer=completer) + '\n'
            tree = parser.parse(expr_str)
        except ParseError:
            prompt = '  '
            continue
        except UnexpectedCharacters as e:
            print(e)
            return List([])
        except KeyboardInterrupt:
            return List([])
        break
    return transformer.transform(tree)


class EvalError(Exception):
    pass


def eval(expr, env):
    # self-evaluating expressions
    if type(expr) in (Integer, Float, String):
        return expr
    # symbols
    elif type(expr) == Symbol:
        if expr == Symbol('#f') or expr == Symbol('#t'):
            return expr
        try:
            return env[str(expr)]
        except KeyError:
            raise EvalError(f'Symbol "{expr}" not found in current environment.')
    elif type(expr) == List:
        op, *args = expr  # unpack
        proc = eval(op, env)
        if type(proc) not in (Procedure, BuiltinProcedure):
            raise EvalError(f'{op} is not a procedure.')
        if type(proc) == BuiltinProcedure:
            return proc.call(env, *args)
            # try:
            #     return proc(env, *args)
            # except TypeError as e:
            #    raise EvalError(str(e))
            # except AssertionError as e:
            #    raise EvalError(str(e))
        else:
            vals = [eval(arg, env) for arg in args]
            if len(vals) != len(proc.arguments):
                raise EvalError(f'Received wrong number of arguments (expected {len(proc.arguments)} and got {len(vals)}).')
            last = List()
            for expr in proc.body:
                last = eval(
                    expr,
                    env.new_child({k: vals[i] for i, k in enumerate(proc.arguments)})
                )
            return last
    else:
        raise ValueError(f'Invalid argument passed to eval: {expr}')


def eval_exprs(expr_list, env):
    results = []
    for expr in expr_list:
        results.append(eval(expr, env))
    return results


def pprint_exprs(expr_list):
    for expr in expr_list:
        if type(expr) == Symbol:
            if expr == Symbol('#t') or expr == Symbol('#f'):
                print(expr)
            else:
                print(f'\'{str(expr)}')
        else:
            print(str(expr))


def repl(env):
    session = PromptSession(
        auto_suggest=AutoSuggestFromHistory(),
        lexer=PygmentsLexer(SchemeLexer),
        style=style_from_pygments_cls(get_style_by_name('monokai')),
        include_default_pygments_style=False,
    )
    while True:
        try:
            pprint_exprs(eval_exprs(read_exprs(session, env), env))
        except EvalError as e:
            print(e)
        except EOFError:
            return
