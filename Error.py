class CompilerException(Exception):
    pass
class LexerException(CompilerException):
    pass
class ParserException(CompilerException):
    pass