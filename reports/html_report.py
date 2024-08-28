import json
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
            for analyzer_name, result in self.analysis_results.items():
                if analyzer_name == "bandit":
                    try:
                        bandit_result = json.loads(result)  # Parse JSON string
                        issue_count = len(bandit_result.get("results", []))
                        if issue_count == 0:
                            f.write(f"<p><span>Bandit:</span> No security issues found.</p>")
                        else:
                            f.write(f"<p><span>Bandit:</span> {issue_count} security issues found.</p>")
                    except json.JSONDecodeError as e:
                        f.write(f"<p><span>Bandit:</span> Failed to parse Bandit results: {e}</p>")
                elif analyzer_name == "mypy":
                    if "Success" in result:
                        f.write(f"<p><span>MyPy:</span> No type issues found.</p>")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(f"<p><span>MyPy:</span> {issue_count} type issues found.</p>")
                elif analyzer_name == "pylint":
                    if "Your code has been rated" in result:
                        issue_count = sum(1 for line in result.splitlines() if "rated at" not in line and line.strip())
                        f.write(f"<p><span>Pylint:</span> {issue_count} issues found.</p>")
                    else:
                        f.write(f"<p><span>Pylint:</span> Issues found. See detailed report below.</p>")
                elif analyzer_name == "flake8":
                    if result.strip() == "":
                        f.write(f"<p><span>Flake8:</span> No issues found.</p>")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(f"<p><span>Flake8:</span> {issue_count} issues found.</p>")
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