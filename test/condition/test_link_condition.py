import unittest
import mock
import json

from src.condition.base_condition import InvalidMember
from src.condition.link_condition import LinkCondition
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
        self.assertTrue(LinkCondition('dogs 1'))
 
        self.assertEqual(Universe.instance().permutations, [
            {'yellow', 'dogs'},
            {'blue', 'cats'},
            {'1', 'yellow'},
            {'blue', '2'},
            {'cats', '2'},
            {'1', 'dogs'}])

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

    def test_eq(self):
        self.fake_dic = {
            'colors': ['white', 'green', 'gold'],
            'pets': ['fish', 'elephant', 'tiger'],
            'nationalities': ['Brazilian', 'Turkish', 'Vietnamese'],
            'foods': ['tofu', 'soy', 'beans']}

        condition1 = LinkCondition('gold fish')
        condition2 = LinkCondition('fish Turkish')
        condition3 = LinkCondition('fish gold')

        self.assertFalse(condition1 == condition2)
        self.assertTrue(condition1 == condition3)

    def test_same_type_link(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(InvalidMember):
            LinkCondition('blue yellow')


if __name__ == '__main__':
    unittest.main()
