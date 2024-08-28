import logging
import os


def analyze_file(file_path, analyzers):
    results = {}
    for name, analyzer in analyzers.items():
        try:
            logging.info(f"Running {name} analysis on {file_path}")
            results[name] = analyzer.analyze(file_path)
        except Exception as e:
            logging.error(f"Error during {name} analysis of {file_path}: {e}")

    return results


def analyze_directory(directory, analyzers):
    ignore_dirs = {'.venv', '.idea', '.git', '__pycache__'}
    analysis_results = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                analysis_results[file_path] = analyze_file(file_path, analyzers)

    return analysis_results
