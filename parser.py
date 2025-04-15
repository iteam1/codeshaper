from lark import Lark, Transformer

lisp_grammar = r"""
    start: expr_list
    expr_list: (expr)*
    ?expr: atom
         | list
    atom: /[a-zA-Z0-9_.+-]+/
    list: "(" expr+ ")"
    %ignore /\s+/
"""

class LispTransformer(Transformer):
    def start(self, items):
        return items
    def atom(self, items):
        token = items[0]
        try:
            return float(token)
        except ValueError:
            return str(token)
    def list(self, items):
        return list(items)
    def expr_list(self, items):
        return items

def parse_lisp(code):
    parser = Lark(lisp_grammar, parser="lalr", transformer=LispTransformer())
    return parser.parse(code)
