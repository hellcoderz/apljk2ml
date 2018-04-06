import sys
import re

def preprocess(token_exprs):
    res = []
    for _type, expr, tag in token_exprs:
        if _type == 0:
            res.append((_type, re.compile(expr), tag))
        else:
            res.append((_type, set(list(expr)), tag))
    return res

def lex(characters, token_exprs):
    pos = 0
    tokens = []

    token_exprs = preprocess(token_exprs)

    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            _type, regex, tag = token_expr
            if _type == 0:
                match = regex.match(characters, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = (text, tag)
                        tokens.append(token)
                    break
            elif _type == 1:
                char_set = regex
                if characters[pos] in char_set:
                    match = True
                    if tag:
                        token = (str(characters[pos]), tag)
                        tokens.append(token)
                    break

        if _type == 0:
            if not match:
                sys.stderr.write('Illegal character: [[ %s ]]' % characters[pos])
                sys.exit(1)
            else:
                pos = match.end(0)
        else:
            if not match:
                sys.stderr.write('Illegal character: [[ %s ]]' % characters[pos])
                sys.exit(1)
            else:
                pos += 1
    return tokens