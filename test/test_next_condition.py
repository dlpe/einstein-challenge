import unittest
import mock
import json

from src.unlink_condition import UnlinkCondition
from src.next_condition import NextCondition
from src.universe import Universe

class TestNextCondition(unittest.TestCase):
    def setUp(self):
        self.fake_dic = {}
        f = mock.MagicMock()
        f.read = lambda: json.dumps(self.fake_dic)

        self.mock_open = mock.patch('src.universe.open', return_value=f)
        self.mock_open.start()

    def tearDown(self):
        self.mock_open.stop()
        Universe.reset()

    def test_next(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue', 'purple', 'green'],
            'pets': ['cats', 'dogs', 'horses', 'capybaras']}

        self.assertTrue(UnlinkCondition('dogs 2'))
        self.assertTrue(UnlinkCondition('dogs 3'))
        self.assertTrue(UnlinkCondition('dogs 4'))
        self.assertTrue(NextCondition('dogs blue'))
        self.assertTrue(NextCondition('capybaras yellow'))

        self.assertTrue({'1', 'dogs'} in Universe.instance().permutations)
        self.assertFalse({'2', 'dogs'} in Universe.instance().permutations)
        self.assertFalse({'3', 'dogs'} in Universe.instance().permutations)
        self.assertFalse({'4', 'dogs'} in Universe.instance().permutations)
        
        self.assertFalse({'1', 'blue'} in Universe.instance().permutations)
        self.assertTrue({'2', 'blue'} in Universe.instance().permutations)
        self.assertFalse({'3', 'blue'} in Universe.instance().permutations)
        self.assertFalse({'4', 'blue'} in Universe.instance().permutations)

        self.assertTrue(NextCondition('blue capybaras'))
        self.assertFalse({'1', 'capybaras'} in Universe.instance().permutations)
        self.assertFalse({'2', 'capybaras'} in Universe.instance().permutations)
        self.assertTrue({'3', 'capybaras'} in Universe.instance().permutations)
        self.assertFalse({'4', 'capybaras'} in Universe.instance().permutations)

        self.assertFalse({'1', 'yellow'} in Universe.instance().permutations)
        self.assertFalse({'2', 'yellow'} in Universe.instance().permutations)
        self.assertFalse({'3', 'yellow'} in Universe.instance().permutations)
        self.assertTrue({'4', 'yellow'} in Universe.instance().permutations)

if __name__ == '__main__':
    unittest.main()
