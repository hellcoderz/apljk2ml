import marisa_trie as mtrie

vocab = [ "=", "=.", "=:", "<", "<.", "<:", ">", ">.", ">:", "_", "_.", "_:", "+", "+.", "+:", "*",
"*.", "*:", "-", "-.", "-:", "%", "%.", "%:", "^", "^.", "^:", "$", "$.", "$:", "~", "~.",
"~:", "|", "|.", "|:", ".", "..", ".:", ":", ":.", "::", ",", ",.", ",:", ";", ";.", ";:",
"#", "#.", "#:", "!", "!.", "!:", "/", "/.", "/:", "\\", "\.", "\:", "[", "[:", "]", "{",
"{.", "{:", "{::", "}", "}.", "}:", "\"", "\".", "\":", "`", "`:", "@", "@.", "@:", "&",
"&.", "&:", "&.:", "?", "?.", "a.", "a:", "A.", "b.", "C.", "d.", "D.", "D:", "e.", "E.",
"f.", "H.", "i.", "i:", "I.", "j.", "L.", "L:", "M.", "o.", "p.", "p..", "p:", "q:", "r.",
"s:", "S:", "t.", "t:", "T.", "u:", "x:", "NB." ]

vocab.sort(lambda x,y: cmp(len(y), len(x)))

alphabets = "abcdefghijklmnopqrstuvwxyz"
alpha = list(alphabets) + list(alphabets.upper())
digit = list("0123456789")
space = [" ", "\t", "\n"]
cbrackets = ["(", ")"]
dot = ["."]
squote = ["'"]


# print len(vocab), len(alpha), len(digit), len(space), len(cbrackets), len(dot)

vocab_trie = mtrie.Trie(vocab)
alpha_trie = mtrie.Trie(alpha)
digit_trie = mtrie.Trie(digit)
space_trie = mtrie.Trie(space)
cbrackets_trie = mtrie.Trie(cbrackets)
dot_trie = mtrie.Trie(dot)
squote_trie = mtrie.Trie(squote)

tries = [
    (u"VOCAB", vocab_trie),
    (u"ALPHA", alpha_trie),
    (u"DIGIT", digit_trie),
    (u"SPACE", space_trie),
    (u"CBRACKETS", cbrackets_trie),
    (u"DOT", dot_trie),
    (u"SQUOTE", squote_trie)
]

def fix(tokens):
    i = 1
    while i < len(tokens) - 1:
        if tokens[i][0] == "." and tokens[i][1] == u"VOCAB":
            if tokens[i-1][1] == u"DIGIT" and tokens[i+1][1] == u"DIGIT":
                tokens[i] = (tokens[i][0], u"DOT")
        i += 1
    return tokens

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        max_len = -1
        temp = None
        for trie in tries:
            p = trie[1].prefixes(expr[i:])
            p.sort()
            if len(p) > 0 and p[-1] == u"NB." and trie[0] == u"VOCAB":
                temp = (expr[i:], u"COMMENT")
                max_len = len(temp[0])
            if len(p) > 0 and len(p[-1]) > max_len:
                temp = (p[-1], trie[0])
                max_len = len(temp[0])
        if temp is not None:
            tokens.append(temp)
        else:
            print "ERROR parsing:", expr[i:]
        i += max_len
    return fix(tokens)

def parse_string(stack, tokens, flag):
    if flag or len(tokens) == 0:
        return stack, tokens, flag
    sbuffer = u""
    sbon = False
    while True:
        value, tag  = tokens.pop(0)
        # generate STRING
        if sbon == True and tag == u"SQUOTE":
            sbon = False
            stack.append((sbuffer, u"STRING"))
            sbuffer = u""
            return stack, tokens, True
#             print "stack=", stack
#             print "tokens=", tokens
#             print "=============================\n"
        elif sbon:
            sbuffer += value
        elif sbon == False and tag == u"SQUOTE":
            sbon = True
        else:
            tokens = [(value, tag)] + tokens
            break
    return stack, tokens, False

def parse_block(stack, tokens, flag):
    if flag or len(tokens) == 0:
        return stack, tokens, flag
    ebuffer = []
    ebon = False
    while True:
        value, tag  = tokens.pop(0)
        # generate BLOCK
        if ebon == True and tag == u"CBRACKETS" and value == u")":
            ebon = False
            stack.append((parse(ebuffer), u"BLOCK"))
            ebuffer = []
            return stack, tokens, True
#             print "stack=", stack
#             print "tokens=", tokens
#             print "=============================\n"
        elif ebon:
            if tag == u"CBRACKETS" and value == u"(":
                tokens = [(value, tag)] + tokens
#                 print "---", tokens
                temp_stack = []
                temp_stack, tokens, flag = parse_block(temp_stack, tokens, False)
#                 print temp_stack, "===", tokens, flag
                if not flag:
                    break
                ebuffer.append(temp_stack[0])
            else:
                ebuffer.append((value, tag))
        elif ebon == False and tag == u"CBRACKETS" and value == u"(":
            ebon = True
        else:
            tokens = [(value, tag)] + tokens
            break
    return stack, tokens, False

def parse_symbol(stack, tokens, flag):
    if flag or len(tokens) == 0:
        return stack, tokens, flag
    symbuffer = u""
    symbon = False
    while True:
        value, tag  = tokens.pop(0)
        # generate SYMBOL
        if symbon == True and tag not in [u"ALPHA", u"DIGIT"]:
            symbon = False
            tokens = [(value, tag)] + tokens
            stack.append((symbuffer, u"SYMBOL"))
            symbuffer = u""
#             print "stack=", stack
#             print "tokens=", tokens
#             print "=============================\n"
        elif symbon == True and len(tokens) == 0:
            symbon = False
            symbuffer += value
            stack.append((symbuffer, u"SYMBOL"))
            symbuffer = u""
            return stack, tokens, True
#             print "stack=", stack
#             print "tokens=", tokens
#             print "=============================\n"
        elif symbon:
            symbuffer += value
        elif symbon == False and tag == u"ALPHA":
            symbon = True
            if len(tokens) == 0:
                tokens = [(value, tag)] + tokens
                continue
            symbuffer += value
        else:
            tokens = [(value, tag)] + tokens
            break
    return stack, tokens, False

def parse_number(stack, tokens, flag):
    if flag or len(tokens) == 0:
        return stack, tokens, flag
    nbuffer = u""
    nbon = False
    ntype = int
    while True:
        value, tag  = tokens.pop(0)
        # generate INT | FLOAT
        if nbon == True and tag not in [u"DIGIT", u"DOT"]:
#             print "END NUMBER BUFFER"
            nbon = False
            tokens = [(value, tag)] + tokens
            if int == ntype:
                stack.append((nbuffer, u"INT"))
            elif float == ntype:
                stack.append((nbuffer, u"FLOAT"))
            nbuffer = u""
            ntype = int
#             print "stack=", stack
#             print "tokens=", tokens
#             print "=============================\n"
        elif nbon == True and tag == "DIGIT" and len(tokens) == 0:
#             print "END NUMBER BUFFER"
            nbon = False
            nbuffer += value
            if int == ntype:
                stack.append((nbuffer, u"INT"))
            elif float == ntype:
                stack.append((nbuffer, u"FLOAT"))
            nbuffer = u""
            ntype = int
            return stack, tokens, True
#             print "stack=", stack
#             print "tokens=", tokens
#             print "=============================\n"
        elif nbon:
#             print "IN NUMBER BUFFER"
            nbuffer += value
            if tag == u"DOT":
                ntype = float
        elif nbon == False and tag == u"DIGIT":
#             print "START NUMBER BUFFER"
            nbon = True
            if len(tokens) == 0:
                tokens = [(value, tag)] + tokens
                continue
            nbuffer += value
        else:
            tokens = [(value, tag)] + tokens
            break
    return stack, tokens, False

def parse_rest(stack, tokens, flag):
    if flag or len(tokens) == 0:
        return stack, tokens, flag
    while True:
        value, tag  = tokens.pop(0)
        # generate vocab
        if tag == u"VOCAB":
            stack.append((value, tag))
            return stack, tokens, True
        elif tag in [u"SPACE", u"COMMENT"]:
            return stack, tokens, True
        else:
            tokens = [(value, tag)] + tokens
            break
    return stack, tokens, False

def parse(expr):
    stack = []
    ntype = int # int | float
    if type(expr) == type([]):
        tokens = expr
    else:
        tokens = tokenize(expr)

    while len(tokens) > 0:

        if tokens[0][1] == u"BLOCK":
            stack.append(tokens.pop(0))

        stack, tokens, flag = parse_string(stack, tokens, False)
#         print "1:", stack, tokens, flag
        stack, tokens, flag = parse_block(stack, tokens, flag)
#         print "2:", stack, tokens, flag
        stack, tokens, flag = parse_symbol(stack, tokens, flag)
#         print "3:", stack, tokens, flag
        stack, tokens, flag = parse_number(stack, tokens, flag)
#         print "4:", stack, tokens, flag
        stack, tokens, flag = parse_rest(stack, tokens, flag)
#         print "5:", stack, tokens, flag

        if not flag and len(tokens) > 0:
            print "ERROR parsing"
            print "stack=", stack
            print "tokens=", tokens
            print "token=", tokens[0]
            break


    return stack

def generate_key(parsed):
    k = []
    for token in parsed:
        if token[1] == u"BLOCK":
            k.append("BLOCK[" + generate_key(token[0]) + "]")
        else:

            k.append(token[1])
    return "|".join(k)


def tokenize_test():
    expr = u"mean1=:(+/%#)1 2 3 4.5 'hello world' 5 E. i.10 (+/ 1 2 3 54.56)"
    expr = u"11 2 3 4.5"
    expr = u"E."
    expr = u"(+/%#)1 2 3 4 i.10 100"
    expr = u"(0 E. i.10) + ?2#10"

    tokens = tokenize(expr)
    for token in tokens:
        print token

def display(tokens, tabs=""):
    for token in tokens:
        if token[1] == u"BLOCK":
            display(token[0], tabs+"\t")
        else:
            print tabs, token

def parse_test(exprs):
    for expr in exprs:
        parsed = parse(expr[0])
    #     for token in parsed:
    #         print token
        if generate_key(parsed) == expr[1]:
            print "TEST PASSED\t", expr[0]
        else:
            print "TEST FAILED\t", expr[0]

if __name__ == "__main__":
    import sys

    exprs = [
        (u"mean1=:(+/%#)1 2 3 4.5 'hello world' 5 E. i.10 (+/ 1 2 3 54.56)",
            u"SYMBOL|VOCAB|BLOCK[VOCAB|VOCAB|VOCAB|VOCAB]|INT|INT|INT|FLOAT|STRING|INT|VOCAB|VOCAB|INT|BLOCK[VOCAB|VOCAB|INT|INT|INT|FLOAT]"),
        (u"11 2 3 4.5", u"INT|INT|INT|FLOAT"),
        (u"E.", u"VOCAB"),
        (u"(+/%#)1 2 3 4 i.10 100", u"BLOCK[VOCAB|VOCAB|VOCAB|VOCAB]INT|INT|INT|INT|VOCAB|INT|INT"),
        (u"(0 E. i.10) + ?2#10", u"BLOCK[INT|VOCAB|VOCAB|INT]|VOCAB|VOCAB|INT|VOCAB|INT"),
        (u"1 2 3 4", u"INT|INT|INT|INT"),
        (u"i.10 100 NB. +/ % #", u"VOCAB|INT|INT"),
        (u"v=: ?. 20 $100     NB. a random vector", u"SYMBOL|VOCAB|VOCAB|INT|VOCAB|INT"),
        (u"quicksort=: (($:@(<#[), (=#[), $:@(>#[)) ({~ ?@#)) ^: (1<#)",
            u"SYMBOL|VOCAB|BLOCK[BLOCK[VOCAB|VOCAB|BLOCK[VOCAB|VOCAB|VOCAB]|VOCAB|BLOCK[VOCAB|VOCAB|BLOCK[VOCAB|VOCAB|VOCAB]]|BLOCK[VOCAB|VOCAB|VOCAB|VOCAB]]|VOCAB|BLOCK[INT|VOCAB|VOCAB]]")
    ]

    if len(sys.argv) == 2:
        expr = sys.argv[1]

        print "Tokenizer Output:"
        for token in tokenize(unicode(expr)):
            print token

        print "\nParser Output:"
        display(parse(unicode(expr)))
    else:
        parse_test(exprs)

    print "\n=============================================================="
    display(parse(exprs[8][0]))
