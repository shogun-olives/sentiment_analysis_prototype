import unittest
from file_helper import extract_metadata as em


class TestMyModule(unittest.TestCase):
    def test_get_symbol(self):
        result = em.get_symbol('Alphabet Inc (GOOGL US Equity)')
        self.assertEqual(result, "GOOGL")


if __name__ == '__main__':
    unittest.main()