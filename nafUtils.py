
from Lexer import Lexer
from Lexer import Grammar

# A epsilon edge ε
EPSILON = -1
# Edges correspond to character sets
CCL = -2
# The corresponding node has two outgoing epsilon sides
EMPTY = -3
ASCII_COUNT = 127
bracketCount = 0

lexer = None


def nfa_builder(regular_string):
    global lexer
    lexer = Lexer(regular_string)
    lexer.advance()  # Grammar.L 默认为普通类型字符
    nfa_StartEnd = nfaStartEnd()
    brackets(nfa_StartEnd)

    return nfa_StartEnd.start_node


class nfaStartEnd(object):
    def __init__(self):
        self.start_node = None
        self.end_node = None


def brackets(nfa_StartEnd):
    global bracketCount
    if lexer.match(Grammar.OPEN_PAREN):  # ‘(’
        bracketCount += 1
        lexer.advance()
        expr(nfa_StartEnd)
        if lexer.match(Grammar.CLOSE_PAREN):  # ‘)’
            lexer.advance()
    elif lexer.match(Grammar.EOS):
        return False
    else:
        expr(nfa_StartEnd)

    while True:
        StartEnd = nfaStartEnd()

        if lexer.match(Grammar.OPEN_PAREN):  # '('
            bracketCount += 1
            lexer.advance()
            expr(StartEnd)
            nfa_StartEnd.end_node.next_1 = StartEnd.start_node
            nfa_StartEnd.end_node = StartEnd.end_node
            if lexer.match(Grammar.CLOSE_PAREN):  # ')'
                lexer.advance()
        elif lexer.match(Grammar.EOS):
            return False
        elif lexer.match(Grammar.AT_BOL):
            lexer.advance()
            brackets(nfa_StartEnd)
        elif lexer.match(Grammar.AT_EOL):
            return False
        else:
            expr(StartEnd)
            nfa_StartEnd.end_node.next_1 = StartEnd.start_node
            nfa_StartEnd.end_node = StartEnd.end_node


# 构建|的 NFA 就是生成两个新节点，新生成的头节点有两条边分别连接到 factor_conn 的头节点，
# 对于两个 factor_conn 的尾节点分别生成一条边连接到新生成的尾节点
def expr(StartEnd):
    factor_conn(StartEnd)
    newStartEnd = nfaStartEnd()

    while lexer.match(Grammar.OR):
        lexer.advance()
        factor_conn(newStartEnd)
        start = nfaNode()
        start.next_1 = newStartEnd.start_node
        start.next_2 = StartEnd.start_node
        StartEnd.start_node = start

        end = nfaNode()
        newStartEnd.end_node.next_1 = end
        StartEnd.end_node.next_2 = end
        StartEnd.end_node = end
    return True


# factor connect
# 一个或者多个 factor 相连接
def factor_conn(StartEnd):
    if is_conn(lexer.current_token):
        factor(StartEnd)

    while is_conn(lexer.current_token):
        newStartEnd = nfaStartEnd()
        factor(newStartEnd)
        StartEnd.end_node.next_1 = newStartEnd.start_node
        StartEnd.end_node = newStartEnd.end_node
    return True


def is_conn(current_token):
    Grammars = [
        Grammar.OPEN_PAREN,
        Grammar.CLOSE_PAREN,
        Grammar.AT_EOL,
        Grammar.EOS,
        Grammar.CLOSURE,
        Grammar.PLUS_CLOSE,
        Grammar.CCL_END,
        Grammar.AT_BOL,
        Grammar.OR,
    ]
    return current_token not in Grammars


# factor * + ? closure
# 先进行 term 的 NFA 的生成，然后根据词法分析器来判断要进行哪个 factor 的 NFA 的构造
def factor(StartEnd):
    # term 的 NFA 的生成
    term(StartEnd)
    # 根据词法分析器来判断要进行哪个 factor 的 NFA 的构造
    if lexer.match(Grammar.CLOSURE):  # *操作就是对之前的 term 再生成两个节点进行连接
        nfa_star_closure(StartEnd)
    elif lexer.match(Grammar.PLUS_CLOSE):  # +
        nfa_plus_closure(StartEnd)
    elif lexer.match(Grammar.OPTIONAL):  # ?
        nfa_option_closure(StartEnd)


# use Bottom-up method
# # Matches. a (single character) []
# 根据当前读入的字符来判断应该构建什么节点
def term(StartEnd):
    if lexer.match(Grammar.L):
        nfa_single_char(StartEnd)  # 普通类型字符
    elif lexer.match(Grammar.ANY):
        nfa_dot_char(StartEnd)


# Match a single character
def nfa_single_char(StartEnd):
    if not lexer.match(Grammar.L):
        return False

    start = StartEnd.start_node = nfaNode()
    StartEnd.end_node = StartEnd.start_node.next_1 = nfaNode()
    start.edge = lexer.lexeme
    lexer.advance()
    return True


# . Matches any single character
def nfa_dot_char(StartEnd):
    if not lexer.match(Grammar.ANY):
        return False

    start = StartEnd.start_node = nfaNode()
    StartEnd.end_node = StartEnd.start_node.next_1 = nfaNode()
    start.edge = CCL
    start.set_input_set()

    lexer.advance()
    return False


# * closure operations
# *操作就是对之前的 term 再生成两个节点进行连接
def nfa_star_closure(StartEnd):
    if not lexer.match(Grammar.CLOSURE):
        return False
    start = nfaNode()
    end = nfaNode()
    start.next_1 = StartEnd.start_node
    start.next_2 = end

    StartEnd.end_node.next_1 = StartEnd.start_node
    StartEnd.end_node.next_2 = end

    StartEnd.start_node = start
    StartEnd.end_node = end

    lexer.advance()
    return True


# + is closure
def nfa_plus_closure(StartEnd):
    if not lexer.match(Grammar.PLUS_CLOSE):
        return False
    start = nfaNode()
    end = nfaNode()
    start.next_1 = StartEnd.start_node

    StartEnd.end_node.next_1 = StartEnd.start_node
    StartEnd.end_node.next_2 = end

    StartEnd.start_node = start
    StartEnd.end_node = end

    lexer.advance()
    return True


# ?
def nfa_option_closure(StartEnd):
    if not lexer.match(Grammar.OPTIONAL):
        return False
    start = nfaNode()
    end = nfaNode()

    start.next_1 = StartEnd.start_node
    start.next_2 = end
    StartEnd.end_node.next_1 = end

    StartEnd.start_node = start
    StartEnd.end_node = end

    lexer.advance()
    return True


def match(str, nfa_machine):
    ls = []
    start_node = nfa_machine
    current_nfa_set = [start_node]
    next_nfa_set = closure(current_nfa_set)

    for i, ch in enumerate(str):
        current_nfa_set = move(next_nfa_set, ch)
        next_nfa_set = closure(current_nfa_set)
        if next_nfa_set is None:
            return ls
        else:
            ls.append(ch)
        if has_accepted_state(next_nfa_set) and i == len(str) - 1:
            return ls

    return None


def move(next_nfa_set, ch):
    out_set = []
    for nfa in next_nfa_set:
        if nfa.edge == ch or (nfa.edge == CCL and ch in nfa.input_set):
            out_set.append(nfa.next_1)
    return out_set


def closure(current_nfa_set):
    if len(current_nfa_set) <= 0:
        return None

    nfa_stack = []
    for i in current_nfa_set:
        nfa_stack.append(i)
    while len(nfa_stack) > 0:
        nfa = nfa_stack.pop()
        next1 = nfa.next_1
        next2 = nfa.next_2
        if next1 is not None and nfa.edge == EPSILON:
            if next1 not in current_nfa_set:
                current_nfa_set.append(next1)
                nfa_stack.append(next1)

        if next2 is not None and nfa.edge == EPSILON:
            if next2 not in current_nfa_set:
                current_nfa_set.append(next2)
                nfa_stack.append(next2)
    return current_nfa_set


# Match success
def has_accepted_state(next_nfa_set):
    for nfa in next_nfa_set:
        if nfa.next_1 is None and nfa.next_2 is None:
            return True


def search(str, nfa_machine, groupID):
    ls = []
    start_node = nfa_machine
    current_nfa_set = [start_node]
    next_nfa_set = closure(current_nfa_set)

    for i, ch in enumerate(str):
        current_nfa_set = move(next_nfa_set, ch)
        next_nfa_set = closure(current_nfa_set)

        if next_nfa_set is None:
            return None
        elif groupID == 0:
            ls.append(ch)
        elif len(current_nfa_set) != 0 and \
                current_nfa_set[0].groupID == groupID:
            ls.append(ch)

        if has_accepted_state(next_nfa_set) and i == len(str) - 1:
            return ls

    return None


# nfa node
class nfaNode(object):
    # Node number
    STATUS_NUM = 0

    def __init__(self):
        self.groupID = bracketCount
        self.edge = EPSILON
        self.next_1 = None
        self.next_2 = None
        self.visited = False
        self.input_set = set()
        self.set_status_num()
        # self.value = None

    def set_status_num(self):
        self.status_num = nfaNode.STATUS_NUM
        nfaNode.STATUS_NUM += 1

    def set_input_set(self):
        self.input_set = set()
        for i in range(ASCII_COUNT):
            self.input_set.add(chr(i))
