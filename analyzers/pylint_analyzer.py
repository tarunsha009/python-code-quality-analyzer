import pylint.lint
from io import StringIO
import sys

import yaml

from utils.config_loader import load_config


class PylintAnalyzer:
    def __init__(self):
        self.config = load_config()
        self.disabled_rules = self.config.get('pylint', {}).get('disable_rules', [])

    def load_disabled_rules(self):
        if self.config_file:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config.get('pylint', {}).get('disable', [])
        return []

    def analyze(self, file_path):
        print(f"Starting Pylint analysis on {file_path}...")  # Debugging print
        pylint_output = StringIO()
        sys.stdout = pylint_output

        try:
            args = [file_path]
            if self.disabled_rules:
                disable_option = f"--disable={','.join(self.disabled_rules)}"
                args.insert(0, disable_option)

            pylint.lint.Run(args)
        except SystemExit as e:  # Pylint may call sys.exit(), catch it here
            print(f"Pylint analysis completed with exit code {e.code}")  # Debugging print

        sys.stdout = sys.__stdout__
        output = pylint_output.getvalue()
        print("Pylint analysis completed.")  # Debugging print
        return output
