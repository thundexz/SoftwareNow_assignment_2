# THIS SECTION IS DONE BY AADIL MOHAMMED FAIZAL

import os

def tokenize(expr):
    """
    A token is a small tuple such as - (TYPE, VALUE)
    """
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        if ch.isspace():
            i += 1

        elif ch.isdigit():
            start = i
            while i < n and expr[i].isdigit():
                i += 1
            if i < n and expr[i] == '.':
                i += 1
                if i < n and expr[i].isdigit():
                    while i < n and expr[i].isdigit():
                        i += 1
                else:
                    return None
            tokens.append(('NUM', expr[start:i]))

        elif ch in '+-*/%^':
            tokens.append(('OP', ch))
            i += 1

        elif ch == '(':
            tokens.append(('LPAREN', '('))
            i += 1

        elif ch == ')':
            tokens.append(('RPAREN', ')'))
            i += 1

        else:
            return None

    tokens.append(('END', ''))
    return tokens

def tokens_to_string(tokens):
    """Turn the token list intotext formats."""
    pieces = []
    for tok_type, tok_val in tokens:
        if tok_type == 'END':
            pieces.append('[END]')
        else:
            pieces.append(f'[{tok_type}:{tok_val}]')
    return ' '.join(pieces)


def evaluate_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []

    for raw_line in lines:
        expr = raw_line.rstrip('\n')
        if expr.strip() == '':
            continue

        tokens = tokenize(expr)

        if tokens is None:
            results.append({
                "input": expr,
                "tree": "ERROR",
                "tokens": "ERROR",
                "result": "ERROR",
            })
            continue

        tok_str = tokens_to_string(tokens)

        tree, pos = parse_expression(tokens, 0)

        if tree is None or tokens[pos][0] != 'END':
            results.append({
                "input": expr,
                "tree": "ERROR",
                "tokens": tok_str,
                "result": "ERROR",
            })
            continue

        tree_str = tree_to_string(tree)
        value = evaluate_tree(tree)

        if value is None:
            results.append({
                "input": expr,
                "tree": tree_str,
                "tokens": tok_str,
                "result": "ERROR",
            })
        else:
            results.append({
                "input": expr,
                "tree": tree_str,
                "tokens": tok_str,
                "result": value,
            })

# Creating the output.txt in the same folder as where the input.txt file is
    folder = os.path.dirname(input_path)
    output_path = os.path.join(folder, 'output.txt') if folder else 'output.txt'

    with open(output_path, 'w', encoding='utf-8') as f:
        for index in range(len(results)):
            entry = results[index]
            f.write(f"Input: {entry['input']}\n")
            f.write(f"Tree: {entry['tree']}\n")
            f.write(f"Tokens: {entry['tokens']}\n")
            if entry['result'] == "ERROR":
                result_str = "ERROR"
            else:
                result_str = format_number(entry['result'])
            f.write(f"Result: {result_str}\n")
            if index < len(results) - 1:
                f.write("\n")

    return results



# THE BELOW SECTION IS DONE BY DARSHANA THAPA





def parse_expression(tokens, pos):

    """Level 1 - Lowest Precedence"""

    node, pos = parse_term(tokens, pos)

    if node is None:

        return None, pos



    while tokens[pos][0] == 'OP' and tokens[pos][1] in ('+', '-'):

        op = tokens[pos][1]

        pos += 1

        right, pos = parse_term(tokens, pos)

        if right is None:

            return None, pos

        node = (op, node, right)



    return node, pos





def parse_term(tokens, pos):

    """Level 2"""

    node, pos = parse_unary(tokens, pos)

    if node is None:

        return None, pos



    while True:

        tok_type, tok_val = tokens[pos]



        if tok_type == 'OP' and tok_val in ('*', '/', '%'):

            pos += 1

            right, pos = parse_unary(tokens, pos)

            if right is None:

                return None, pos

            node = (tok_val, node, right)



        elif tok_type == 'LPAREN':

            right, pos = parse_unary(tokens, pos)

            if right is None:

                return None, pos

            node = ('*', node, right)



        else:

            break



    return node, pos





def parse_unary(tokens, pos):

    """Level 3"""

    tok_type, tok_val = tokens[pos]



    if tok_type == 'OP' and tok_val == '-':

        pos += 1

        operand, pos = parse_unary(tokens, pos)

        if operand is None:

            return None, pos

        return ('neg', operand), pos



    return parse_power(tokens, pos)





def parse_power(tokens, pos):

    """Level 4 Highest Precedence"""

    node, pos = parse_primary(tokens, pos)

    if node is None:

        return None, pos



    tok_type, tok_val = tokens[pos]

    if tok_type == 'OP' and tok_val == '^':

        pos += 1

        right, pos = parse_unary(tokens, pos)

        if right is None:

            return None, pos

        node = ('^', node, right)



    return node, pos





def parse_primary(tokens, pos):

    tok_type, tok_val = tokens[pos]



    if tok_type == 'NUM':

        return ('num', float(tok_val)), pos + 1



    if tok_type == 'LPAREN':

        node, pos = parse_expression(tokens, pos + 1)

        if node is None:

            return None, pos

        if tokens[pos][0] != 'RPAREN':

            return None, pos

        return node, pos + 1



    return None, pos





def tree_to_string(node):

    tag = node[0]



    if tag == 'num':

        return format_number(node[1])



    if tag == 'neg':

        return f"(neg {tree_to_string(node[1])})"



    left_str = tree_to_string(node[1])

    right_str = tree_to_string(node[2])

    return f"({tag} {left_str} {right_str})"





def evaluate_tree(node):

    tag = node[0]



    if tag == 'num':

        return node[1]



    if tag == 'neg':

        value = evaluate_tree(node[1])

        if value is None:

            return None

        return -value



    left = evaluate_tree(node[1])

    right = evaluate_tree(node[2])

    if left is None or right is None:

        return None



    if tag == '+':

        return left + right

    if tag == '-':

        return left - right

    if tag == '*':

        return left * right

    if tag == '/':

        if right == 0:

            return None

        return left / right

    if tag == '%':

        if right == 0:

            return None

        return left % right

    if tag == '^':

        return left ** right



    return None





def format_number(value):

    """Whole numbers with no decimal point, else rounded to 4 decimals."""

    if value == int(value):

        return str(int(value))

    return str(round(value, 4))





if __name__ == "__main__":
   current_folder = os.path.dirname(os.path.abspath(__file__))
   input_path = os.path.join(current_folder, "sample_input.txt")

   results = evaluate_file(input_path)

   for r in results:
        print(r)


   for r in results:

        print(r)

