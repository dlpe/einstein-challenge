import unittest
import mock
import json

from src.link_condition import LinkCondition
from src.universe import Universe

class TestLinkCondition(unittest.TestCase):
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
            'pets': ['cats', 'dogs']}

        self.assertTrue(LinkCondition('dogs yellow'))
        self.assertEqual(Universe.instance().permutations, [
            {'yellow', 'dogs'},
            {'blue', 'cats'}
        ])


    def test_linked_members(self):
        self.fake_dic = {
            'colors': ['white', 'green', 'gold'],
            'pets': ['fish', 'elephant', 'tiger'],
            'nationalities': ['Brazilian', 'Turkish', 'Vietnamese'],
            'foods': ['tofu', 'soy', 'beans']}

        LinkCondition('gold fish')
        LinkCondition('fish Turkish')
        LinkCondition('gold tofu')

        self.assertEqual(LinkCondition.linked_to('tofu'), {
            'gold',
            'fish',
            'Turkish'})

if __name__ == '__main__':
    unittest.main()
