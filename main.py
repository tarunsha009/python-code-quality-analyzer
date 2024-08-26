from analyzers.pylint_analyzer import PylintAnalyzer
from analyzers.flake8_analyzer import Flake8Analyzer
from reports.html_report import HTMLReport
from reports.json_report import JSONReport


def main():
    # Example analysis with Pylint
    pylint_analyzer = PylintAnalyzer()
    pylint_results = pylint_analyzer.analyze("example.py")

    # Example analysis with Flake8
    flake8_analyzer = Flake8Analyzer()
    flake8_results = flake8_analyzer.analyze("example.py")

    # Print the results to the console for debugging
    print("Pylint Results:\n", pylint_results)
    print("Flake8 Results:\n", flake8_results)

    # Generate reports
    html_report = HTMLReport(pylint_results)
    html_report.generate("pylint_report.html")

    html_report = HTMLReport(flake8_results)
    html_report.generate("flake8_results.html")

    json_report = JSONReport({"pylint": pylint_results, "flake8": flake8_results})
    json_report.generate("combined_report.json")


if __name__ == "__main__":
    main()
