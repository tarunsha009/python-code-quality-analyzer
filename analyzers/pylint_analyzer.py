import pylint.lint
from io import StringIO
import sys


class PylintAnalyzer:
    def __init__(self, config_file=None):
        self.config_file = config_file

    def analyze(self, file_path):
        print(f"Starting Pylint analysis on {file_path}...")  # Debugging print
        pylint_output = StringIO()
        sys.stdout = pylint_output

        try:
            args = [file_path]
            if self.config_file:
                args.insert(0, f'--rcfile={self.config_file}')
            pylint.lint.Run(args)
        except SystemExit as e:  # Pylint may call sys.exit(), catch it here
            print(f"Pylint analysis completed with exit code {e.code}")  # Debugging print

        sys.stdout = sys.__stdout__
        output = pylint_output.getvalue()
        print("Pylint analysis completed.")  # Debugging print
        return output


if __name__ == "__main__":
    analyzer = PylintAnalyzer()
    result = analyzer.analyze("example.py")
    print(result)
