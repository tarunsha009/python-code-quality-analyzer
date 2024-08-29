import logging

import pylint.lint
from io import StringIO
import sys

import yaml

from utils.config_loader import load_config


class PylintAnalyzer:
    def __init__(self):
        self.config = load_config()
        self.disabled_rules = self.config.get('pylint', {}).get('disable_rules', [])
        self.results = {
            "issues": 0,
            "details": "",
            "score": None,
        }

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
            logging.info(f"Pylint analysis completed with exit code {e.code}")  # Debugging print
        finally:
            sys.stdout = sys.__stdout__
        output = pylint_output.getvalue()
        # self.results["issues"] = self.count_issues(output)
        # self.results["details"] = self.extract_relevant_output(output)
        # self.results["score"] = self.extract_score(output)

        return output

    def count_issues(self, output):
        # Count only the lines that indicate issues (ignoring the final rating line)
        issue_count = 0
        capture_issues = False
        for line in output.splitlines():
            if line.startswith("************* Module"):
                capture_issues = True
            elif line.startswith("------------------------------------------------------------------"):
                capture_issues = False
            elif capture_issues and line.strip():
                issue_count += 1
        return issue_count

    def extract_relevant_output(self, output):
        # Extract the lines between the start of the issue block and the end delimiter
        relevant_lines = []
        capture_issues = False
        for line in output.splitlines():
            if line.startswith("************* Module"):
                capture_issues = True
            elif line.startswith("------------------------------------------------------------------"):
                capture_issues = False
            if capture_issues or line.startswith("Your code has been rated at"):
                relevant_lines.append(line)
        return "\n".join(relevant_lines)

    @staticmethod
    def extract_score(output):
        for line in output.splitlines():
            if "Your code has been rated at" in line:
                return line.split(" ")[-2]  # Extracting the score value
        return None
