import re
import subprocess
import logging


class IsortAnalyzer:
    def analyze(self, file_path):
        print(f"Starting Isort analysis on {file_path}...")
        command = ['isort', '--check-only', '--diff', file_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Isort analysis completed for {file_path}. No issues found.")
                return "Isort: No issues found."
            else:
                logging.info(f"Isort analysis completed for {file_path}. Issues found.")
                cleaned_output = self._clean_terminal_output(result.stdout)
                if not cleaned_output.strip():  # If output is empty, provide a fallback message
                    return "Isort: Issues found, but no specific details provided."
                return cleaned_output
        except Exception as e:
            logging.error(f"Error running Isort on {file_path}: {e}")
            return f"Error running Isort: {e}"

    def _clean_terminal_output(self, output):
        """
        Remove terminal color codes and unnecessary escape sequences from the output.
        """
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', output)