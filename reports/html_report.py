from reports.report import Report


class HTMLReport(Report):
    def generate(self, output_file):
        summary = self.extract_summary()

        with open(output_file, "w") as f:
            f.write("""
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #2c3e50; }
                    h2 { color: #16a085; }
                    pre { background-color: #ecf0f1; padding: 10px; border-radius: 5px; }
                    .summary { font-size: 1.1em; margin-bottom: 20px; }
                    .summary span { font-weight: bold; }
                    .issue { margin-bottom: 15px; }
                </style>
            </head>
            <body>
                <h1>Code Quality Report</h1>
            """)

            # Summary Section
            f.write("<div class='summary'><h2>Summary</h2>")
            for analyzer_name, issue_count in summary.items():
                f.write(f"<p><span>{analyzer_name.capitalize()} Issues:</span> {issue_count}</p>")
            f.write("</div>")

            # Detailed Results
            for analyzer_name, result in self.analysis_results.items():
                f.write(f"<h2>{analyzer_name.capitalize()} Results</h2>")
                f.write("<pre class='issue'>")
                f.write(result)
                f.write("</pre>")

            f.write("""
            </body>
            </html>
            """)


if __name__ == "__main__":
    # Example usage
    analysis_results = {
        "pylint": "Example Pylint data\nError1\nError2",
        "flake8": "Example Flake8 data\nError1\nError2\nError3",
    }
    report = HTMLReport(analysis_results)
    report.generate("report.html")
