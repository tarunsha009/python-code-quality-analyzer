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


def main():
    config = load_config()
    if config is None:
        return

    setup_logging(config['logging']['file'], config['logging']['level'])

    analyzers = {}

    if config['analyzers']['pylint']:
        from analyzers.pylint_analyzer import PylintAnalyzer
        analyzers['pylint'] = PylintAnalyzer()

    if config['analyzers']['flake8']:
        from analyzers.flake8_analyzer import Flake8Analyzer
        analyzers['flake8'] = Flake8Analyzer()

    if config['analyzers'].get('bandit', True):  # Add Bandit support by default
        from analyzers.bandit_analyzer import BanditAnalyzer
        analyzers['bandit'] = BanditAnalyzer()

    if config['analyzers'].get('mypy', True):  # Add mypy support by default
        from analyzers.mypy_analyzer import MyPyAnalyzer
        analyzers['mypy'] = MyPyAnalyzer()

    if config['analyzers'].get('safety', True):
        from analyzers.safety_analyzer import SafetyAnalyzer
        analyzers['safety'] = SafetyAnalyzer()

    if config['analyzers'].get('isort', True):
        from analyzers.isort_analyzer import IsortAnalyzer
        analyzers['isort'] = IsortAnalyzer()

    if config['analyzers'].get('vulture', True):
        from analyzers.vulture_analyzer import VultureAnalyzer
        analyzers['vulture'] = VultureAnalyzer()

    analysis_results = {}

    # input_path = "C:\\Users\\Richa\\PycharmProjects\\Design Patterns"
    input_path = "C:\\Users\\Richa\\PycharmProjects\\code_quality_analyzer\\example.py"
    report_type = "html"

    try:
        if os.path.isdir(input_path):
            analysis_results = analyze_directory(input_path, analyzers)
            for file_path, results in analysis_results.items():
                generate_report(report_type, results, os.path.basename(file_path).split(".")[0])
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
