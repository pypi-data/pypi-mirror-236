import unittest
from brams import locations

class TestLocations(unittest.TestCase):

    def test_multiply_by_three(self):

        all = locations.all()
        self.assertEqual(type(all), dict)

unittest.main()