import unittest
from analyzers.pylint_analyzer import PylintAnalyzer


class TestPylintAnalyzer(unittest.TestCase):
    def test_analyze(self):
        analyzer = PylintAnalyzer()
        result = analyzer.analyze("example.py")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
