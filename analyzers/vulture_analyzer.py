import subprocess
import logging


class VultureAnalyzer:
    def __init__(self, config_file=None):
        self.config_file = config_file

    def analyze(self, file_path):
        print(f"Starting Vulture analysis on {file_path}...")
        command = ['vulture', file_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            logging.info(f"Vulture analysis completed for {file_path}.")
            return result.stdout
        except Exception as e:
            logging.error(f"Error running Vulture on {file_path}: {e}")
            return f"Error running Vulture: {e}"
