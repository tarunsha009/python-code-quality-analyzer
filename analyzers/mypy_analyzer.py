import logging
import subprocess


class MyPyAnalyzer:

    def __init__(self, config_file=None):
        self.config_file = config_file

    def analyze(self, file_path):
        print(f"Starting Mypy analysis on {file_path}...")  # Debugging print
        command = ['mypy', file_path, '--ignore-missing-imports', '--show-error-codes']
        if self.config_file:
            command.extend(['--config-file', self.config_file])

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            logging.info(f"MyPy analysis completed for {file_path}")
            return result.stdout
        except Exception as e:
            logging.error(f"Error running MyPy on {file_path}: {e}")
            return f"Error running MyPy: {e}"
