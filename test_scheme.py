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
    Procedure
)

def parse_str(s):
    return scheme.transformer.transform(scheme.parser.parse(s))

def test_parsing():
    # symbols
    assert parse_str(r'foobar') == [Symbol('foobar')]
    assert parse_str(r'    foobar    ') == [Symbol('foobar')]
    # strings
    assert parse_str(r'"hello world"') == [String("hello world")]
    assert parse_str(r'"hello\nworld"') == [String("hello\nworld")]
    # integers
    assert parse_str(r"123") == [123]
    assert parse_str(r"-42") == [-42]
    # floats
    assert parse_str(r"3.14159265359") == [3.14159265359]
    assert parse_str(r"-2.7") == [-2.7]
    assert parse_str(r"2.99e8") == [2.99e8]
    # quote
    assert parse_str(r"'foobar") == [List([Symbol('quote'), Symbol('foobar')])]
    assert parse_str(r"'123") == [List([Symbol('quote'), Integer(123)])]
    assert parse_str(r"'()") == [List([Symbol('quote'), List([])])]
    # list
    assert parse_str(r'(1 2 3)') == [[1, 2, 3]]
    assert parse_str(r"('a 2 3)") == [List([[Symbol('quote'), Symbol('a')], 2, 3])]
    assert parse_str("(+\n1\n2)") == [List([Symbol('+'), 1, 2])]
    assert parse_str("(define (add a b) (+ a b))") == [['define', ['add', 'a', 'b'], ['+', 'a', 'b']]]
