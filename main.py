import sys
import os
from Lexer.Lexer import Lexer
from ParserExpr.Parser import Parser
from Error import CompilerException

# -l -f Lexer/input.txt
# -l -d Lexer/Tests
# -p -f ParserExpr/input.txt
# -p -d ParserExpr/Tests
inp = sys.argv[1:]
type_analysis = ""
type_reader = ""
path = ""
for el in inp:
    if el == "-l":
        type_analysis = "lexer"
    if el == "-p":
        type_analysis = "parser"
    if el == "-f":
        type_reader = "file"
    if el == "-d":
        type_reader = "dir"
    if os.path.isfile(el) or os.path.isdir(el):
        path = el

if type_analysis == "lexer":
    if type_reader == "file":
        if os.path.isfile(path):
            try:
                lexer = Lexer(path)
                token = lexer.next_lexem()
                if token.get_type() != "eof":
                    print(token.get_str())
                while token.get_type() != "eof":
                    token = lexer.next_lexem()
                    if token.get_type() != "eof":
                        print(token.get_str())
            except CompilerException as error:
                print(error)
    elif type_reader == "dir":
        if os.path.isdir(path):
            count = 0
            count_failed = 0
            for file in os.listdir(path):
                if file.endswith("(code).txt"):
                    count += 1
                    abs_path = path + "/" + file
                    abs_path_output = abs_path.replace("(code)", "(output)")
                    abs_path_correct = abs_path.replace("(code)", "(correct)")
                    file_output = open(abs_path_output, "w+", encoding="utf-8")
                    file_output.seek(0)
                    file_output.truncate()
                    file_correct = open(abs_path_correct, "r", encoding="utf-8")
                    try:
                        lexer = Lexer(abs_path)
                        token = lexer.next_lexem()
                        if token.get_type() != "eof":
                            file_output.write(token.get_str())
                        while token.get_type() != "eof":
                            token = lexer.next_lexem()
                            if token.get_type() != "eof":
                                file_output.write("\n" + token.get_str())
                    except CompilerException as error:
                        if file_output.tell():
                            file_output.write("\n" + str(error))
                        else:
                            file_output.write(str(error))
                    file_output.close()
                    file_output = open(abs_path_output, "r", encoding="utf-8")
                    output = file_output.read()
                    correct = file_correct.read()
                    if output == correct:
                        print(f"{count}. {file} - ok")
                    else:
                        print(f"{count}. {file} - wrong")
                        count_failed += 1
            print(f"Всего тестов: {count}")
            print(f"Провалено тестов: {count_failed}")
elif type_analysis == "parser":
    if type_reader == "file":
        if os.path.isfile(path):
            try:
                lexer = Lexer(path)
                lexer.next_lexem()
                parser = Parser(lexer).parse_expr()
                print(parser.get_str())
            except CompilerException as error:
                print(error)
    elif type_reader == "dir":
        if os.path.isdir(path):
            count = 0
            count_failed = 0
            for file in os.listdir(path):
                if file.endswith("(code).txt"):
                    count += 1
                    abs_path = path + "/" + file
                    abs_path_output = abs_path.replace("(code)", "(output)")
                    abs_path_correct = abs_path.replace("(code)", "(correct)")
                    file_output = open(abs_path_output, "w+", encoding="utf-8")
                    file_output.seek(0)
                    file_output.truncate()
                    file_correct = open(abs_path_correct, "r", encoding="utf-8")
                    try:
                        lexer = Lexer(abs_path)
                        lexer.next_lexem()
                        parser = Parser(lexer).parse_expr()
                        file_output.write(parser.get_str())
                    except CompilerException as error:
                        file_output.write(str(error))
                    file_output.close()
                    file_output = open(abs_path_output, "r", encoding="utf-8")
                    output = file_output.read()
                    correct = file_correct.read()
                    if output == correct:
                        print(f"{count}. {file} - ok")
                    else:
                        print(f"{count}. {file} - wrong")
                        count_failed += 1
            print(f"Всего тестов: {count}")
            print(f"Провалено тестов: {count_failed}")
