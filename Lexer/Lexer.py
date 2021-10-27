from Lexer.Token import Token
from Error import LexerException


class Lexer:
    def __init__(self, path):
        self.file = open(path, "r", encoding="utf-8")
        self.line = 1
        self.column = 1
        self.keep_coord()
        self.symb = self.file.read(1)
        self.state = "undefined"
        self.reserved = ["array", "asm", "begin", "case", "const", "constructor", "destructor", "do",
                         "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                         "in", "inherited", "inline", "interface", "label", "library", "nil", "object",
                         "of", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                         "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor",
                         "abs", "arctan", "boolean", "char", "cos", "dispose", "eof", "eoln", "exp",
                         "false", "get", "input", "integer", "ln", "maxint", "new", "output",
                         "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite",
                         "sin", "sqr", "sqrt", "succ", "text", "true", "unpack", "write", "writeln"]

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
            if self.state == "undefined":
                if [" ", "\n", "\t", "\r"].count(self.symb):
                    if self.symb == "\n":
                        self.next_line()
                    self.next_symb()
                elif self.symb.isalpha():
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = "identifier"
                    self.next_symb()
                elif self.symb.isdigit():
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = "int"
                    self.next_symb()
                elif self.symb == "'":
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = "string"
                    self.next_symb()
                elif self.symb == "#":
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = "string literal"
                    self.next_symb()
                elif ["+", "-", "*", "/"].count(self.symb):
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = "operations"
                    self.next_symb()
                elif self.symb == "{":
                    self.state = "multiline comment"
                    self.next_symb()
                elif ['.', ',', ':', ';', '(', ')', '[', ']'].count(self.symb):
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = "separators"
                    self.next_symb()
                else:
                    self.keep_coord()
                    self.buf += self.symb
                    self.state = "error"
                    self.next_symb()

            elif self.state == "identifier":
                if self.symb.isalpha() or self.symb.isdigit() or self.symb == "_":
                    self.buf += self.symb
                    self.next_symb()
                else:
                    self.state = "undefined"
                    if self.reserved.count(self.buf.lower()):
                        self.token = Token(self.coord, "зарезервированное слово", self.buf, self.buf.lower())
                    elif ['div', 'mod'].count(self.buf.lower()):
                        self.token = Token(self.coord, "операция", self.buf, self.buf.lower())
                    else:
                        self.token = Token(self.coord, "идентификатор", self.buf, self.buf.lower())
                    return self.token
            elif self.state == "int":
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb == ".":
                    self.buf += self.symb
                    self.next_symb()
                    self.state = "real"
                elif self.symb.lower() == "e":
                    self.buf += self.symb
                    self.next_symb()
                    self.state = "real_e"
                else:
                    self.state = "undefined"
                    self.token = Token(self.coord, "целое число", self.buf, int(self.buf))
                    return self.token
            elif self.state == "real":
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb.lower() == "e":
                    if self.buf.endswith('.'):
                        self.state = "error"
                    self.buf += self.symb
                    self.next_symb()
                    self.state = "real_e"
                else:
                    if self.buf.endswith('.'):
                        self.state = "error"
                    else:
                        self.state = "undefined"
                        self.token = Token(self.coord, "вещественное число", self.buf, float(self.buf))
                        return self.token
            elif self.state == "real_e":
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                    self.state = "read_degree"
                elif ['+', '-'].count(self.symb):
                    self.buf += self.symb
                    self.next_symb()
                    self.state = "read_sign"
                else:
                    self.state = "error"
            elif self.state == "read_sign":
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                    self.state = "read_degree"
                else:
                    self.state = "error"
            elif self.state == "read_degree":
                if self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                else:
                    self.state = "undefined"
                    self.token = Token(self.coord, "вещественное число", self.buf, float(self.buf))
                    return self.token

            elif self.state == "string":
                if self.symb == "\n" or not self.symb:
                    tab = " " * 8
                    raise LexerException(f"{self.coord}{tab}Lexical error: {self.buf}")
                if self.symb != "'":
                    self.buf += self.symb
                    self.next_symb()
                else:
                    self.state = "undefined"
                    self.buf += self.symb
                    self.next_symb()
                    if self.symb == "#":
                        self.buf += self.symb
                        self.next_symb()
                        self.state = "string literal"
                    else:
                        self.token = Token(self.coord, "строка", self.buf, self.replace_literal(self.buf))
                        return self.token
            elif self.state == "string literal":
                if self.symb == "#" and self.buf[len(self.buf) - 1].isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb.isdigit():
                    self.buf += self.symb
                    self.next_symb()
                elif self.symb == "'" and self.buf[len(self.buf) - 1].isdigit():
                    self.buf += self.symb
                    self.next_symb()
                    self.state = "string"
                else:
                    self.state = "undefined"
                    self.next_symb()
                    self.token = Token(self.coord, "строка", self.buf, self.replace_literal(self.buf))
                    return self.token

            elif self.state == "operations":
                if self.symb == "*" and self.buf == "*":
                    self.state = "undefined"
                    self.buf += self.symb
                    self.next_symb()
                    self.token = Token(self.coord, "операция", self.buf, self.buf)
                    return self.token
                elif self.symb == "/" and self.buf == "/":
                    self.state = "one line comment"
                    self.next_symb()
                    self.buf = ""
                else:
                    self.state = "undefined"
                    self.token = Token(self.coord, "операция", self.buf, self.buf)
                    return self.token
            elif self.state == "one line comment":
                if self.symb != "\n":
                    self.next_symb()
                else:
                    self.state = "undefined"
            elif self.state == "multiline comment":
                if self.symb == "\n":
                    self.next_line()
                    self.next_symb()
                elif self.symb != "}":
                    self.next_symb()
                else:
                    self.state = "undefined"
                    self.next_symb()
            elif self.state == "separators":
                self.state = "undefined"
                if self.buf == ':' and self.symb == '=':
                    self.buf += self.symb
                    self.next_symb()
                    self.token = Token(self.coord, "операция", self.buf, self.buf)
                    return self.token
                self.token = Token(self.coord, "сепаратор", self.buf, self.buf)
                return self.token
            elif self.state == "error":
                if not [" ", "\n", "\t", "\r", '.', ',', ':', ';', '(', ')', '[', ']', ''].count(self.symb):
                    self.buf += self.symb
                    self.next_symb()
                else:
                    tab = " " * 8
                    raise LexerException(f"{self.coord}{tab}Lexical error: {self.buf}")
        self.keep_coord()
        self.token = Token(self.coord, "eof", "", "")
        return self.token
