import unittest
import mock
import json

from src.unlink_condition import UnlinkCondition
from src.universe import Universe

class TestUnlinkCondition(unittest.TestCase):
    def setUp(self):
        self.fake_dic = {}
        f = mock.MagicMock()
        f.read = lambda: json.dumps(self.fake_dic)

        self.mock_open = mock.patch('src.universe.open', return_value=f)
        self.mock_open.start()

    def tearDown(self):
        self.mock_open.stop()
        Universe.reset()

    def test_unlink(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs'],
            'cars': ['Toyota', 'Ford']}

        self.assertTrue(UnlinkCondition('dogs yellow'))
        self.assertTrue(UnlinkCondition('Ford cats'))
        self.assertTrue(UnlinkCondition('dogs 2'))

        self.assertEqual(Universe.instance().permutations, [
            {'yellow', 'cats'},
            {'blue', 'dogs'},
            {'yellow', 'Toyota'},
            {'blue', 'Ford'},
            {'yellow', '2'},
            {'blue', '1'},
            {'cats', 'Toyota'},
            {'dogs', 'Ford'},
            {'cats', '2'},
            {'dogs', '1'},
            {'2', 'Toyota'},
            {'1', 'Ford'}])


if __name__ == '__main__':
    unittest.main()
