import os

from analyzers.pylint_analyzer import PylintAnalyzer
from analyzers.flake8_analyzer import Flake8Analyzer
from reports.html_report import HTMLReport
from reports.json_report import JSONReport


def analyze_file(file, pylint_analyzer, flake8_analyzer):
    print(f"Analyzing {file}")
    pylint_results = pylint_analyzer.analyze(file)
    flake8_results = flake8_analyzer.analyze(file)
    return pylint_results, flake8_results


def generate_report(report_type, analysis_results, file_name):
    report_map = {
        "html": HTMLReport,
        "json": JSONReport,
    }

    report_class = report_map.get(report_type)
    if not report_class:
        print(f"Unsupported report type: {report_type}")
        return

    report = report_class(analysis_results)
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    output_file = os.path.join(results_dir, f"{file_name}_report.{report_type}")
    report.generate(output_file)


def analyze_directory(directory, pylint_analyzer, flake8_analyzer, report_type):
    ignore_dirs = {'.venv', '.idea', '.git', '__pycache__'}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                analysis_results = {}
                analysis_results['pylint'], analysis_results['flake8'] = analyze_file(file_path, pylint_analyzer, flake8_analyzer)
                generate_report(report_type, analysis_results, file.split(".")[0])


def main():
    pylint_analyzer = PylintAnalyzer()
    flake8_analyzer = Flake8Analyzer()

    analysis_results = {}

    input_path = "C:\\Users\\Richa\\PycharmProjects\\Design Patterns"
    report_type = "html"

    if os.path.isdir(input_path):
        analyze_directory(input_path, pylint_analyzer, flake8_analyzer, report_type)
    elif os.path.isfile(input_path) and input_path.endswith(".py"):
        analysis_results['pylint'], analysis_results['flake8'] = analyze_file(input_path, pylint_analyzer, flake8_analyzer)
        generate_report(report_type, analysis_results, os.path.basename(input_path).split(".")[0])
    else:
        print("Invalid Path Provided. Please enter a valid Path.")


if __name__ == "__main__":
    main()
