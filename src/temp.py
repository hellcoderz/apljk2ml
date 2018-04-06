from lark import Lark

grammar = """
    INTEGER : /[0-9]+/
    FLOAT: INTEGER "." INTEGER
    WHITESPACE: (" " | /\t/ )+
    SYMBOL: /[a-zA-Z]+/
    STRING: /["][ a-zA-Z]+["]/
    list: (FLOAT | INTEGER | STRING)+
    ATOM: FLOAT | INTEGER | STRING
    VERBS: "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "_" | "-" 
        | "+" | "=" | "'" | ";" | ":" | "?" | "/" | ">" | "<" | "," | "." 
        | "\\" | "[" | "]" | "{" | "}" | "(" | ")" | "`" | "~"
    expr: expr VERBS expr 
        | VERBS expr
        | list
        | ATOM
    ASSIGN: "=." | "=:"
    start: SYMBOL ASSIGN expr
        | SYMBOL ASSIGN
        | expr
    %ignore WHITESPACE
"""

parser = Lark(grammar, start="start")

print parser.parse('mean=:5+1 2 3 4')
