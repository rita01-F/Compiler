from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def get_str(self, level=1):
        pass


class IdentifierNode(Node):
    def __init__(self, token):
        self.token = token

    def get_str(self, level=1):
        return (f"{self.token.get_value()}")


class IntNode(Node):
    def __init__(self, token):
        self.token = token

    def get_str(self, level=1):
        return (f"{self.token.get_value()}")


class RealNode(Node):
    def __init__(self, token):
        self.token = token

    def get_str(self, level=1):
        return (f"{self.token.get_value()}")


class UnOpNode(Node):
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand

    def get_str(self, level=1):
        return (f"{self.operation.get_value()}{self.operand.get_str()}")


class BinOpNode(Node):
    def __init__(self, operation, operand_1, operand_2):
        self.operation = operation
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def get_str(self, level=1):
        tab = " " * 4
        operand_1 = self.operand_1.get_str(level + 1)
        operand_2 = self.operand_2.get_str(level + 1)
        operation = self.operation.get_value()
        return (f"{operation}\n"
                f"{tab * level}{operand_1}\n"
                f"{tab * level}{operand_2}")
