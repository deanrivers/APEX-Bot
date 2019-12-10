import unittest
import process

class TestProcess(unittest.TestCase):
    def test_splitString(self):
        string = process.newProcess('j')
        self.isinstance(string, str)


if __name__ == '__main__':
    unittest.main()