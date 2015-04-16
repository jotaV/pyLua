import sys, getopt

from tokenClasses import Comment, Especial, Identifier, Keyword, \
    Number, Operator, String, Whitespace, Token

token_class_list = [
    Comment, Whitespace, Keyword, Identifier, Operator, Especial, Number, String
]

def analyze(text, verbose_mode = 0):
    """Analyze the text passed

        Keyword arguments:
        text -- the text that will be analyzed
        verbose_mode -- how outup information.
            '0' only the final result,
            '1' all tokens generate,
            '2' the tokens before of the erro message

        return a list of tokens in the text
    """

    token_list = []
    token = None

    offset = 0
    span = 0
    i = 0

    while offset < len(text):
        while not token:

            if i < len(token_class_list):
                (token, span) = token_class_list[i].match(text, offset)
                i += 1

            else:
                print(
                    "\n Erro Lexico na linha %d coluna %d" % \
                    (Token.current_line_number + 1, offset - Token.current_line_offset) \
                )
                return None

        if verbose_mode == 2:
            print(token)

        token_list.append(token)
        token = None
        offset = span
        i = 0

    if verbose_mode == 1:
        for token in token_list:
            print(token)

    print('\n Scanner finalizado com sucesso!')

    return token_list

def main(argv):
    verbose_mode = 0

    try:
        file_name = argv[0]
    except IndexError:
        print('pyLuaScanner.py <file.lua>')
        return None

    try:
        opts, args = getopt.getopt(argv[1:], 'vV')
    except getopt.GetoptError:
        print('pyLuaScanner.py <file.lua>')
        return None

    if ('-V', '') in opts:
        verbose_mode = 2
    elif ('-v', '') in opts:
        verbose_mode = 1

    file = open(file_name, 'r')
    analyze(file.read(), verbose_mode)

if __name__ == "__main__":
    main(sys.argv[1:])
