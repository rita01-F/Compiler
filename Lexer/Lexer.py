from Lexer.Token import Token
from Error import LexerException


class Lexer:
    def __init__(self, path):
        self.file = open(path, "r", encoding="utf-8")
        self.line = 1
        self.column = 1
        self.keep_coord()
        self.symb = self.file.read(1)

        self.reserved = ["array", "asm", "begin", "case", "const", "constructor", "destructor", "do",
                         "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                         "in", "inherited", "inline", "interface", "label", "library", "nil", "object",
                         "of", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                         "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor",
                         "abs", "arctan", "boolean", "char", "cos", "dispose", "eof", "eoln", "exp",
                         "false", "get", "input", "integer", "ln", "maxint", "new", "output",
                         "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite",
                         "sin", "sqr", "sqrt", "succ", "text", "true", "unpack", "write", "writeln"]
        self.undefined = "undefined"
        self.identifier = "identifier"
        self.reserved_word = "reserved word"
        self.integer = "integer"
        self.integer16 = "integer 16"
        self.integer8 = "integer 8"
        self.integer2 = "integer 2"
        self.real = "real"
        self.real_e = "real e"
        self.real_degree = "real degree"
        self.real_sign = "real sign"
        self.string = "string"
        self.string_literal = "string literal"
        self.operation = "operation"
        self.separator = "separator"
        self.one_line_comment = "one line comment"
        self.multiline_comment = "multiline comment"
        self.multiline_comment_2 = "multiline comment2"
        self.error = "error"
        self.state = self.undefined

    def next_line(self):
        self.line += 1
        self.column = 0

    def next_symb(self):
        self.symb = self.file.read(1)
        self.column += 1

    def keep_coord(self):
        self.coord = [self.line, self.column]

    def current_lexem(self):
        return self.token

    def replace_literal(self, string):
        array = string.split("'")
        output = "'"
        for i, el in enumerate(array):
            if i % 2 == 0:
                buf = ""
                for v in el:
                    if v == "#":
                        if buf:
                            output += chr(int(buf))
                            buf = ""
                    else:
                        buf += v
                if buf:
                    output += chr(int(buf))
            else:
                output += el
        return output + "'"

    def next_lexem(self):
        self.buf = ""
        while self.symb or self.buf:
            if self.state == self.undefined:
                if [" ", "\n", "\t", "\r"].count(self.symb):
                    if self.symb == "\n":
                        self.next_line()
                    self.next_symb()
                elif self.symb.isalpha():
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.identifier
                    self.next_symb()
                elif self.symb.isdigit():
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.integer
                    self.next_symb()
                elif self.symb == "$":
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.integer16
                    self.next_symb()
                elif self.symb == "&":
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.integer8
                    self.next_symb()
                elif self.symb == "%":
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.integer2
                    self.next_symb()
                elif self.symb == "'":
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.string
                    self.next_symb()
                elif self.symb == "#":
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.string_literal
                    self.next_symb()
                elif ["+", "-", "*", "/", "<", ">", "="].count(self.symb):
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.operation
                    self.next_symb()
                elif self.symb == "{":
                    self.state = self.multiline_comment
                    self.next_symb()
                elif ['.', ',', ':', ';', '(', ')', '[', ']'].count(self.symb):
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.separator
                    self.next_symb()
                else:
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = self.error
                    self.next_symb()

            elif self.state == self.identifier:
                if self.symb.isalpha() or self.symb.isdigit() or self.symb == "_":
                    self.buf += self.symb
                    self.next_symb()
                else:
                    self.state = self.undefined
                    if self.reserved.count(self.buf.lower()):
                        self.token = Token(self.coord, self.reserved_word, self.buf, self.buf.lower())
                    elif ['div', 'mod'].count(self.buf.lower()):
                        self.token = Token(self.coord, self.operation, self.buf, self.buf.lower())
                    else:
                        self.token = Token(self.coord, self.identifier, self.buf, self.buf.lower())
                    return self.token
            elif self.state == self.integer:
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb == ".":
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.real
                elif self.symb.lower() == "e":
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.real_e
                else:
                    self.state = self.undefined
                    self.token = Token(self.coord, self.integer, self.buf, int(self.buf))
                    return self.token
            elif self.state == self.integer16:
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif "a" <= self.symb.lower() <= "f":
                    self.buf += self.symb
                    self.next_symb()
                else:
                    if len(self.buf) == 1:
                        tab = "\t" * 2
                        raise LexerException(f"{self.coord}{tab}Lexical error: {self.buf}")
                    self.state = self.undefined
                    self.token = Token(self.coord, self.integer16, self.buf, int(self.buf[1:], 16))
                    return self.token
            elif self.state == self.integer8:
                if self.symb.isdigit():
                    if 0 <= int(self.symb) <= 7:
                        self.buf += self.symb
                        self.next_symb()
                    else:
                        self.state = self.error
                else:
                    if len(self.buf) == 1:
                        tab = "\t" * 2
                        raise LexerException(f"{self.coord}{tab}Lexical error: {self.buf}")
                    self.state = self.undefined
                    self.token = Token(self.coord, self.integer8, self.buf, int(self.buf[1:], 8))
                    return self.token
            elif self.state == self.integer2:
                if self.symb.isdigit():
                    if 0 <= int(self.symb) <= 1:
                        self.buf += self.symb
                        self.next_symb()
                    else:
                        self.state = self.error
                else:
                    if len(self.buf) == 1:
                        tab = "\t" * 2
                        raise LexerException(f"{self.coord}{tab}Lexical error: {self.buf}")
                    self.state = self.undefined
                    self.token = Token(self.coord, self.integer2, self.buf, int(self.buf[1:], 2))
                    return self.token
            elif self.state == self.real:
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb.lower() == "e":
                    if self.buf.endswith('.'):
                        self.state = self.error
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.real_e
                else:
                    if self.buf.endswith('.'):
                        self.state = self.error
                    else:
                        self.state = self.undefined
                        self.token = Token(self.coord, self.real, self.buf, float(self.buf))
                        return self.token
            elif self.state == self.real_e:
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.real_degree
                elif ['+', '-'].count(self.symb):
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.real_sign
                else:
                    self.state = self.error
            elif self.state == self.real_sign:
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.real_degree
                else:
                    self.state = self.error
            elif self.state == self.real_degree:
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                else:
                    self.state = self.undefined
                    self.token = Token(self.coord, self.real, self.buf, float(self.buf))
                    return self.token

            elif self.state == self.string:
                if self.symb == "\n" or not self.symb:
                    tab = "\t" * 2
                    raise LexerException(f"{self.coord}{tab}Lexical error: {self.buf}")
                if self.symb != "'":
                    self.buf += self.symb
                    self.next_symb()
                else:
                    self.state = self.undefined
                    self.buf += self.symb
                    self.next_symb()
                    if self.symb == "#":
                        self.buf += self.symb
                        self.next_symb()
                        self.state = self.string_literal
                    else:
                        self.token = Token(self.coord, self.string, self.buf, self.replace_literal(self.buf))
                        return self.token
            elif self.state == self.string_literal:
                if self.symb == "#" and self.buf[len(self.buf) - 1].isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb == "'" and self.buf[len(self.buf) - 1].isdigit():
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.string
                else:
                    self.state = self.undefined
                    self.next_symb()
                    self.token = Token(self.coord, self.string, self.buf, self.replace_literal(self.buf))
                    return self.token

            elif self.state == self.operation:
                if ['**', '<=', '<>', '>=', '<<', '>>'].count(self.buf + self.symb):
                    self.state = self.undefined
                    self.buf += self.symb
                    self.next_symb()
                    self.token = Token(self.coord, self.operation, self.buf, self.buf)
                    return self.token
                elif self.symb == "/" and self.buf == "/":
                    self.state = self.one_line_comment
                    self.next_symb()
                    self.buf = ""
                else:
                    self.state = self.undefined
                    self.token = Token(self.coord, self.operation, self.buf, self.buf)
                    return self.token
            elif self.state == self.one_line_comment:
                if self.symb != "\n":
                    self.next_symb()
                else:
                    self.state = self.undefined
            elif self.state == self.multiline_comment:
                if self.symb == "\n":
                    self.next_line()
                    self.next_symb()
                elif self.symb != "}":
                    self.next_symb()
                else:
                    self.state = self.undefined
                    self.next_symb()
            elif self.state == self.multiline_comment_2:
                if self.symb == "\n":
                    self.next_line()
                    self.next_symb()
                elif not (self.buf.endswith("*") and self.symb == ")"):
                    self.buf += self.symb
                    self.next_symb()
                else:
                    self.state = self.undefined
                    self.next_symb()
                    self.buf = ""
            elif self.state == self.separator:
                self.state = self.undefined
                if self.buf == ':' and self.symb == '=':
                    self.buf += self.symb
                    self.next_symb()
                    self.token = Token(self.coord, self.operation, self.buf, self.buf)
                    return self.token
                elif self.buf == '(' and self.symb == '*':
                    self.buf += self.symb
                    self.next_symb()
                    self.state = self.multiline_comment_2
                else:
                    self.token = Token(self.coord, self.separator, self.buf, self.buf)
                    return self.token
            elif self.state == self.error:
                if not [" ", "\n", "\t", "\r", '.', ',', ':', ';', '(', ')', '[', ']', ''].count(self.symb):
                    self.buf += self.symb
                    self.next_symb()
                else:
                    tab = "\t" * 2
                    raise LexerException(f"{self.coord}{tab}Lexical error: {self.buf}")
        self.keep_coord()
        self.token = Token(self.coord, "eof", "", "")
        return self.token
