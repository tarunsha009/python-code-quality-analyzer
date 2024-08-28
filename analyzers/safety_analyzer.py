import logging
import subprocess


class SafetyAnalyzer:

    def __init__(self, config_file = None):
        self.config_file = config_file

    def analyze(self, file_path):
        print(f"Starting Safety analysis on {file_path}...")
        command = ['safety', 'check', '--json']
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            logging.info("Safety analysis completed.")
            return result.stdout
        except Exception as e:
            logging.error(f"Error running Safety: {e}")
            return f"Error running Safety: {e}"
