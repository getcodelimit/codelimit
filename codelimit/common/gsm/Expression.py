from  codelimit.common.gsm.Atom import Atom
from  codelimit.common.gsm.Concat import Concat
from  codelimit.common.gsm.NFA import NFA
from  codelimit.common.gsm.Operator import Operator


def expression_to_nfa(expression: list[Operator | str]) -> NFA:
    op_expression = [Atom(item) if isinstance(item, str) else item for item in expression]
    nfa_stack = []
    for item in op_expression:
        item.apply(nfa_stack)
        Concat().apply(nfa_stack)

    return nfa_stack.pop()
