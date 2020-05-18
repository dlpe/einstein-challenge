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

    def test_link(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs'],
            'cars': ['Toyota', 'Ford']}

        self.assertTrue(UnlinkCondition('dogs yellow'))
        self.assertTrue(UnlinkCondition('Ford cats'))
        self.assertEqual(Universe.instance().permutations, [
            {'cats', 'yellow'},
            {'blue', 'dogs'},
            {'Toyota', 'yellow'},
            {'blue', 'Ford'},
            {'cats', 'Toyota'},
            {'dogs', 'Ford'}])


if __name__ == '__main__':
    unittest.main()
