
import unittest
from hypothesis import given, strategies
from RegularExpression import RegularExpression


class testRegularExpression(unittest.TestCase):

    def test_match_w(self):
        # test \w
        str = "abc2"
        reg = "abc\\w"
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_match_s(self):
        # test \s
        str = "abc "
        reg = "abc\\s"
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_match_d(self):
        # test \d
        str = "abc9"
        reg = "abc\\d"
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_match_start(self):
        # test ^
        str = "abc"
        reg = "^abc"
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_match_point(self):
        # test .
        str = "abcd"
        reg = "abc."
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_match_multiplication(self):
        # test *
        str = "abcddddddd"
        reg = "abcd*"
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_match_plus(self):
        # test +
        str = "abcdd"
        reg = "abcd+"
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_match_why(self):
        # test ? | (  )
        str = "bbbbbbbbbb"
        reg = "(\\*?|b+)"
        reg_result = RegularExpression(str, reg).match()
        self.assertEqual(str, reg_result)

    def test_position_multiplication(self):
        # test *  position(search)
        str = "abcddddddd"
        reg = "abcd*"
        reg_result, start, end = RegularExpression(str, reg).position()
        self.assertEqual(True, reg_result)
        self.assertEqual(start, 9)
        self.assertEqual(end, 9)

    def test_split(self):
        # test split aaaaabcccccasdzxc
        str = 'hwhwhwhwhaaaaabcccccasdzxc'
        reg = '(\\*?|a+)(zx|bc*)(asd|fgh)(zxc)'
        result = RegularExpression(str, reg).split()
        self.assertEqual(result, "aaaaabcccccasdzxc")


if __name__ == "__main__":
    unittest.main()
