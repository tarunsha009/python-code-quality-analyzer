import json
import logging
import os
import subprocess


class SafetyAnalyzer:

    def __init__(self, config_file = None):
        self.config_file = config_file

    def analyze(self, file_path):
        print(f"Starting Safety analysis on {file_path}...")
        requirements_file = os.path.join(file_path, 'requirements.txt')
        command = ['safety', 'check', '--json']

        if os.path.exists(requirements_file):
            command.extend(['-r', requirements_file])
            logging.info(f"Using requirements file: {requirements_file} for Safety analysis.")
        else:
            logging.info("No requirements.txt found. Analyzing installed packages in the virtual environment.")
            return
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            logging.info("Safety analysis completed.")
            safety_results = json.loads(result.stdout)
            return safety_results
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing Safety results: {e}")
            return {"errors": [f"Error parsing Safety results: {e}"]}
        except Exception as e:
            logging.error(f"Error running Safety: {e}")
            return {"errors": [f"Error running Safety: {e}"]}


if __name__ == "__main__":
    abcs = SafetyAnalyzer()
    result = abcs.analyze("C:\\Users\\Richa\\PycharmProjects\\Blog_Platform")
    print(r)