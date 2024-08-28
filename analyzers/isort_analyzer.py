import subprocess
import logging


class IsortAnalyzer:
    def analyze(self, file_path):
        print(f"Starting Isort analysis on {file_path}...")
        command = ['isort', '--check-only', file_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Isort analysis completed for {file_path}. No issues found.")
                return "Isort: No issues found."
            else:
                logging.info(f"Isort analysis completed for {file_path}. Issues found.")
                return result.stdout
        except Exception as e:
            logging.error(f"Error running Isort on {file_path}: {e}")
            return f"Error running Isort: {e}"
