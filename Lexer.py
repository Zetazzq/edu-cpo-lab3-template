

# This file contains a lexical analyzer

from enum import Enum
# Token


class Grammar(Enum):
    EOS = 0
    ANY = 1
    AT_BOL = 2
    AT_EOL = 3
    CCL_END = 4
    CCL_START = 5
    CLOSE_CURLY = 6
    CLOSE_PAREN = 7
    CLOSURE = 8
    DASH = 9
    END_OF_INPUT = 10
    L = 11
    OPEN_CURLY = 12
    OPEN_PAREN = 13
    OPTIONAL = 14
    OR = 15
    PLUS_CLOSE = 16


# 正则的语法
Grammars = {
    '.': Grammar.ANY,  # 1
    '^': Grammar.AT_BOL,  # 2
    '$': Grammar.AT_EOL,  # 3
    ')': Grammar.CLOSE_PAREN,  # 7
    '*': Grammar.CLOSURE,  # 8
    '(': Grammar.OPEN_PAREN,  # 13
    '|': Grammar.OR,  # 15
    '+': Grammar.PLUS_CLOSE,  # 16
}
# Lexical analyzer


class Lexer(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self.lexeme = ''
        self.pos = 0
        self.isescape = False
        self.current_token = None
    # 进入下一个状态

    def advance(self):
        pos = self.pos
        pattern = self.pattern
        if pos > len(pattern) - 1:
            self.current_token = Grammar.EOS
            return Grammar.EOS

        text = self.lexeme = pattern[pos]
        # Handle escape characters

        if text == '\\':

            self.isescape = not self.isescape
            self.pos = self.pos + 1
            self.current_token = self.haes()
        else:
            self.current_token = self.semantic(text)

        return self.current_token

    def haes(self):
        expr = self.pattern.lower()
        pos = self.pos
        ev = {
            '\0': '\\',
            'b': '\b',
            'f': '\f',
            'n': '\n',
            's': ' ',
            't': '\t',
            'e': '\033',
            'w': '2',
            'd': '9',
        }

        rval = ev.get(expr[pos])

        if rval is None:
            if expr[pos] == '^':
                rval = self.tip()
            else:
                rval = expr[pos]
        self.pos = self.pos + 1
        self.lexeme = rval
        return Grammar.L

    def semantic(self, text):
        self.pos = self.pos + 1
        return Grammars.get(text, Grammar.L)  # 没有则返回默认值

    def tip(self):
        self.pos = self.pos + 1
        return self.pattern[self.pos] - '@'

    def match(self, token):
        return self.current_token == token
