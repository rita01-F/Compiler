from Error import ParserException
from ParserExpr.Node import IntNode, IdentifierNode, BinOpNode, UnOpNode, RealNode


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tab = " " * 8

    def parse_expr(self):
        token = self.lexer.current_lexem()
        if token.get_type() == "eof":
            raise ParserException(f"{token.get_coord()}{self.tab}Syntax error: unexpected eof")
        operand_1 = self.parse_term()
        operation = self.lexer.current_lexem()
        while ["+", "-"].count(operation.get_value()):
            self.lexer.next_lexem()
            operand_2 = self.parse_term()
            operand_1 = BinOpNode(operation, operand_1, operand_2)
            operation = self.lexer.current_lexem()
        return operand_1

    def parse_term(self):
        operand_1 = self.parse_factor()
        operation = self.lexer.current_lexem()
        while ["*", "/"].count(operation.get_value()):
            self.lexer.next_lexem()
            operand_2 = self.parse_factor()
            operand_1 = BinOpNode(operation, operand_1, operand_2)
            operation = self.lexer.current_lexem()
        return operand_1

    def parse_factor(self):
        token = self.lexer.current_lexem()
        self.lexer.next_lexem()
        if token.get_type() == "identifier":
            return IdentifierNode(token)
        elif token.get_type() == "integer":
            return IntNode(token)
        elif token.get_type() == "real":
            return RealNode(token)
        elif ["+", "-"].count(token.get_value()):
            operand = self.parse_expr()
            return UnOpNode(token, operand)
        elif token.get_value() == "(":
            operand_1 = self.parse_expr()
            token = self.lexer.current_lexem()
            if token.get_value() != ")":
                raise ParserException(f"{token.get_coord()}{self.tab}Syntax error: ')' was expected")
            self.lexer.next_lexem()
            return operand_1
        raise ParserException(f"{token.get_coord()}{self.tab}Syntax error: {token.get_code()}")
