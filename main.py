import concurrent.futures
import logging
import os

from analyzers.analyzer_manager import analyze_directory, analyze_file
from reports.html_report import HTMLReport
from reports.json_report import JSONReport
from reports.markdown_report import MarkdownReport
from reports.pdf_report import PDFReport
from utils.config_loader import load_config
from utils.logger import setup_logging


def generate_report(report_type, analysis_results, file_name):
    report_map = {
        "html": HTMLReport,
        "json": JSONReport,
        'markdown': MarkdownReport,
        'pdf': PDFReport
    }

    report_class = report_map.get(report_type)
    if not report_class:
        logging.error(f"Unsupported report type: {report_type}")
        print(f"Unsupported report type: {report_type}")
        return
    try:
        report = report_class(analysis_results)
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        output_file = os.path.join(results_dir, f"{file_name}_report.{report_type}")
        report.generate(output_file)
        logging.info(f"Report generated: {output_file}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        print(f"Error: File not found - {e}")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        print(f"Error: Permission denied - {e}")
    except Exception as e:
        logging.error(f"Failed to generate report for {file_name}: {e}")
        print(f"Failed to generate report for {file_name}: {e}")


def setup_analyzers(config):
    analyzers = {}

    if config['analyzers'].get('pylint', True):
        from analyzers.pylint_analyzer import PylintAnalyzer
        analyzers['pylint'] = PylintAnalyzer()

    if config['analyzers'].get('flake8', True):
        from analyzers.flake8_analyzer import Flake8Analyzer
        analyzers['flake8'] = Flake8Analyzer()

    if config['analyzers'].get('bandit', True):
        from analyzers.bandit_analyzer import BanditAnalyzer
        analyzers['bandit'] = BanditAnalyzer()

    if config['analyzers'].get('mypy', True):
        from analyzers.mypy_analyzer import MyPyAnalyzer
        analyzers['mypy'] = MyPyAnalyzer()

    if config['analyzers'].get('isort', True):
        from analyzers.isort_analyzer import IsortAnalyzer
        analyzers['isort'] = IsortAnalyzer()

    if config['analyzers'].get('vulture', True):
        from analyzers.vulture_analyzer import VultureAnalyzer
        analyzers['vulture'] = VultureAnalyzer()

    if config['analyzers'].get('safety', True):
        from analyzers.safety_analyzer import SafetyAnalyzer
        analyzers['safety'] = SafetyAnalyzer()

    return analyzers


def main():
    config = load_config()
    if config is None:
        return

    setup_logging(config['logging']['file'], config['logging']['level'])

    input_path = config.get('input', {}).get('path', None)
    report_type = config.get('input', {}).get('report_type', 'html')

    if not input_path:
        logging.error("No input path provided in the configuration.")
        print("No input path provided in the configuration.")
        return

    paths_to_process = []
    ignore_dirs = {'.venv', '.idea', '.git', '__pycache__', 'venv'}
    if os.path.isdir(input_path):
        for root, dirs, files in os.walk(input_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith(".py"):
                    paths_to_process.append(os.path.join(root, file))
            for dir in dirs:
                paths_to_process.append(os.path.join(root, dir))
    elif os.path.isfile(input_path) and input_path.endswith(".py"):
        paths_to_process.append(input_path)
    else:
        logging.error("Invalid path provided. Please enter a valid Python file or directory.")
        print("Invalid path provided. Please enter a valid Python file or directory.")
        return

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, setup_analyzers(config), path, report_type) for path in
                   paths_to_process]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing a path: {e}")
                print(f"Error processing a path: {e}")
    print("abc")


def process_file(analyzers, input_path, report_type):
    try:
        if os.path.isdir(input_path):
            analysis_results = analyze_directory(input_path, analyzers)
            if 'safety' in analyzers:
                safety_results = analyzers['safety'].analyze(input_path)
                analysis_results['safety'] = {'safety': safety_results}
            for file_path, results in analysis_results.items():
                file_name = 'Packages_analysis' if file_path == 'safety' else os.path.basename(file_path).split(".")[0]
                generate_report(report_type, results, file_name)
        elif os.path.isfile(input_path) and input_path.endswith(".py"):
            results = analyze_file(input_path, analyzers)
            generate_report(report_type, results, os.path.basename(input_path).split(".")[0])
        else:
            logging.error("Invalid path provided. Please enter a valid Python file or directory.")
            print("Invalid path provided. Please enter a valid Python file or directory.")
    except Exception as e:
        logging.error(f"Error occurred during analysis: {e}")
        print(f"Error occurred during analysis: {e}")


if __name__ == "__main__":
    main()
