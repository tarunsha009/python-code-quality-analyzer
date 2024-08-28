import logging
import subprocess


class BanditAnalyzer:

    def __init__(self, config_file=None):
        self.config_file = config_file

    def analyze(self, file_path):
        print(f"Starting Bandit analysis on {file_path}...")  # Debugging print
        command = ['bandit', '-r', file_path, '-f', 'json']

        if self.config_file:
            command.extend(['-c', self.config_file])

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            logging.info(f"Bandit analysis completed for {file_path}")
            return result.stdout
        except Exception as e:
            logging.error(f"Error running Bandit on {file_path}: {e}")
            return f"Error running Bandit: {e}"
