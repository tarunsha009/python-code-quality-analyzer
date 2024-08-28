import subprocess


class Flake8Analyzer:
    def __init__(self, config_file=None):
        self.config_file = config_file

    def analyze(self, file_path):
        command = ["flake8", file_path]
        if self.config_file:
            command.insert(1, f'--config={self.config_file}')
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
