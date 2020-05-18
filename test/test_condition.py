import unittest
import mock
import json

from src.condition import (
    Condition,
    InvalidMember,
    NoMatchLeftException)

from src.universe import Universe

class TestCondition(unittest.TestCase):
    def setUp(self):
        self.fake_dic = {}
        f = mock.MagicMock()
        f.read = lambda: json.dumps(self.fake_dic)

        self.mock_open = mock.patch('src.universe.open', return_value=f)
        self.mock_open.start()

    def tearDown(self):
        self.mock_open.stop()
        Universe.reset()

    def test_inexistent(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(InvalidMember):
            Condition('fish yellow')

    def test_same_type_link(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(InvalidMember):
            Condition('blue yellow')

    def test_nomatchexception(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        Universe.instance().permutations.remove({'yellow', 'dogs'})
        Universe.instance().permutations.remove({'yellow', 'cats'})

        with self.assertRaises(NoMatchLeftException):
            Condition.linked_to('yellow')

    def test_eq(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        condition1 = Condition('yellow dogs')
        condition2 = Condition('blue cats')
        condition3 = Condition('dogs yellow')
        condition4 = Condition('dogs yellow')

        self.assertFalse(condition1 == condition2)
        self.assertTrue(condition1 == condition3)
        self.assertTrue(condition3 == condition4)

    def test_repr(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        self.assertEqual(str(Condition('yellow dogs')), 'yellow dogs')


if __name__ == '__main__':
    unittest.main()
