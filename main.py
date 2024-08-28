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


def generate_report(filename, pylint_results, flake8_results, report_type):
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    if report_type == "html":
        output_file = os.path.join(results_dir, f"{filename}_report.html")
        html_report = HTMLReport(pylint_results, flake8_results)
        html_report.generate(output_file)
    elif report_type == "json":
        output_file = os.path.join(results_dir, f"{filename}_combined_report.json")
        json_report = JSONReport({"pylint": pylint_results, "flake8": flake8_results})
        json_report.generate(output_file)
    else:
        print("Unsupported File Type")


def analyze_directory(directory, pylint_analyzer, flake8_analyzer, report_type):
    ignore_dirs = {'.venv', '.idea', '.git', '__pycache__'}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                pylint_results, flake8_results = analyze_file(file_path, pylint_analyzer, flake8_analyzer)
                generate_report(file.split(".")[0], pylint_results, flake8_results, report_type)


def main():
    pylint_analyzer = PylintAnalyzer()
    flake8_analyzer = Flake8Analyzer()

    input_path = "C:\\Users\\Richa\\PycharmProjects\\Design Patterns"
    report_type = "html"

    if os.path.isdir(input_path):
        analyze_directory(input_path, pylint_analyzer, flake8_analyzer, report_type)
    elif os.path.isfile(input_path) and input_path.endswith(".py"):
        pylint_results, flake8_results = analyze_file(input_path, pylint_analyzer, flake8_analyzer)
        generate_report(input_path.split(".")[0], pylint_results, flake8_results, report_type)
    else:
        print("Invalid Path Provided. Please enter a valid Path.")


if __name__ == "__main__":
    main()
