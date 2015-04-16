import re

class Token():
    current_line_number = 0
    current_line_offset = 0

    def __init__(self, token_class, content, offset):
        self.token_class = token_class
        self.content = content
        self.line = Token.current_line_number + 1
        self.column = offset - Token.current_line_offset

    def __str__(self):
        return "( %10s, %15s, (%d,%2d) )" %  (self.token_class.__name__, \
            self.content if self.content else ' '*5 + '-----' + ' '*5, \
            self.line, self.column \
        )

class TokenClass():
    expression = None

    @classmethod
    def match(cls, string, offset):
        match_obj = cls.expression.match(string, offset)

        if match_obj:
            token = Token(cls, match_obj.group(), offset)
            return token, match_obj.span()[1]

        else:
            return None, 0


class Whitespace(TokenClass):
    expression = re.compile(r'\s+')

    @classmethod
    def match(cls, string, offset):
        match_obj = cls.expression.match(string, offset)

        if match_obj:
            token = Token(cls, "", offset)
            last_match = None

            for last_match in re.finditer(r'\n', match_obj.group()):
                Token.current_line_number += 1

            if last_match: Token.current_line_offset = offset + last_match.end()
            return token, match_obj.span()[1]
        else:
            return None, 0


class Keyword(TokenClass):
    keywords_blocks = r'(do|end|return|break)'
    keywords_expressions = r'(nil|false|true|in)'
    keywords_control_structures = \
        r'(for|if|then|elseif|else|while|repeat|until|local|function)'

    expression = re.compile(keywords_blocks + r'|' + keywords_expressions + r'|' \
        + keywords_control_structures)


class Identifier(TokenClass):
    expression = re.compile(r'[a-zA-Z_]\w*')


class Number(TokenClass):
    digit = r'[0-9]'
    digits = digit + r'+'
    opt_fraction = r'(\.' + digits + r')?'
    opt_exponent = r'(e[+|-]?' + digits + r')?'

    expression = re.compile(
        r'-?' + digits + opt_fraction + opt_exponent + r'(?=[^a-z|A-Z_])'
    )


class String(TokenClass):
    string_content = r'(\w|\W)*?'
    normal_string = r'(?P<ss>[\'|\"])' + string_content + r'(?<!\\)(?P=ss)'
    paragraph_string = r'\[\[' + string_content + r'\]\]'

    expression = re.compile(normal_string + r'|' + paragraph_string)

    @classmethod
    def match(cls, string, offset):
        match_obj = cls.expression.match(string, offset)

        if match_obj:
            token = Token(cls, match_obj.group(), offset)
            last_match = None

            for last_match in re.finditer(r'\n', match_obj.group()):
                Token.current_line_number += 1

            if last_match: Token.current_line_offset = offset + last_match.end()

            return token, match_obj.span()[1]

        else:
            return None, 0


class Operator(TokenClass):
    arithmetic_operators = r'(-|\+|\*|/|\^|%)'
    relational_operators = r'(==|~=|<|>|<=|>=)'
    logical_operators = r'(not|or|and)'
    other_operators = r'(\.\.\.|\.\.|\.|:|#|=)'

    expression = re.compile(
        arithmetic_operators + r'|' + relational_operators + r'|' + \
        logical_operators + r'|' + other_operators
    )


class Especial(TokenClass):
    expression = re.compile(r'(\(|\)|\{|\}|\[|\]|;|,)')


class Comment(Whitespace):
    comment_line = r'(--(?!\[\[))(.)*(\n|$)'
    comment_block = r'(--\[\[(.|\s)*?)\]\]'

    expression = re.compile(comment_line + r'|' + comment_block)
