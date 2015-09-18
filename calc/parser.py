import re

from tdparser import Lexer, Token
from math import log

class Integer(Token):
    def __init__(self, text):
        self.value = int(text)

    def nud(self, context):
        """What the token evaluates to"""
        return self.value

class Float(Token):
    def __init__(self, text):
        self.value = float(text)

    def nud(self, context):
        """What the token evaluates to"""
        return self.value

class Addition(Token):
    lbp = 10  # Precedence

    def led(self, left, context):
        """Compute the value of this token when between two expressions."""
        # Fetch the expression to the right, stoping at the next boundary
        # of same precedence
        right_side = context.expression(self.lbp)
        return left + right_side

class Substraction(Token):
    lbp = 10  # Same precedence as addition

    def led(self, left, context):
        return left - context.expression(self.lbp)

    def nud(self, context):
        """When a '-' is present on the left of an expression."""
        # This means that we are returning the opposite of the next expression
        return - context.expression(self.lbp)

class Multiplication(Token):
    lbp = 20  # Higher precedence than addition/substraction

    def led(self, left, context):
        return left * context.expression(self.lbp)

class Division(Token):
    lbp = 20  # Same precedence as Multiplication

    def led(self, left, context):
        return left / context.expression(self.lbp)

class Power(Token):
    lbp = 30  # Higher than mult

    def led(self, left, context):
        # We pick expressions with a lower precedence, so that
        # 2 ** 3 ** 2 computes as 2 ** (3 ** 2)
        return left ** context.expression(self.lbp - 1)

class Log(Token):
    lbp = 30  # Higher than mult

    def nud(self, context):
        return log(float(context.expression(self.lbp - 1)))

lexer = Lexer(with_parens=True)
lexer.register_token(Integer, re.compile(r'\d+'))
lexer.register_token(Float, re.compile(r'\d+\.\d+'))
lexer.register_token(Addition, re.compile(r'\+'))
lexer.register_token(Substraction, re.compile(r'-'))
lexer.register_token(Multiplication, re.compile(r'\*'))
lexer.register_token(Division, re.compile(r'/'))
lexer.register_token(Power, re.compile(r'\*\*'))
lexer.register_token(Log, re.compile(r'log'))

def parse(text):
    return lexer.parse(text)
