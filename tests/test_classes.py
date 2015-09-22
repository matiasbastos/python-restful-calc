import pytest
from .conftests import testapp
from calc.parser import parse

@pytest.mark.usefixtures("testapp")
class TestClasses:
    def test_parser_sum(self, testapp):
        c = parse('2+2')
        assert c == 4

    def test_parser_rest(self, testapp):
        c = parse('5-2')
        assert c == 3

    def test_parser_multiplication(self, testapp):
        c = parse('5*2')
        assert c == 10

    def test_parser_division(self, testapp):
        c = parse('10/2')
        assert c == 5

    def test_parser_power(self, testapp):
        c = parse('2**2')
        assert c == 4

    def test_parser_log(self, testapp):
        c = parse('log2')
        assert c == 0.6931471805599453

    def test_parser_big_result(self, testapp):
        c = parse('4.013048009299565*10**76')
        assert c == 4.013048009299565e+76

    def test_parser_combinated_calc(self, testapp):
        c = parse('(2+2)*log10/3')
        assert c == 3.0701134573253945
