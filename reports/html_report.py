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
                    .summary { font-size: 1.1em; margin-bottom: 20px; }
                    .good { color: green; }
                    .warning { color: orange; }
                    .bad { color: red; }
                    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                    th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
                    th { background-color: #f4f4f4; }
                    .center { text-align: center; }
                </style>
            </head>
            <body>
                <h1>Code Quality Report</h1>
            """)

            # Summary Table Section
            f.write("<div class='summary'><h2>Summary</h2>")
            f.write("""
            <table>
                <tr>
                    <th>Analyzer</th>
                    <th>Status</th>
                    <th>Issues</th>
                    <th>Comments</th>
                </tr>
            """)
            for analyzer_name, result in self.analysis_results.items():
                if analyzer_name == "bandit":
                    try:
                        bandit_result = json.loads(result)  # Parse JSON string
                        issue_count = len(bandit_result.get("results", []))
                        if issue_count == 0:
                            f.write(f"<tr><td>Bandit</td><td class='good center'>Good</td><td class='center'>0</td><td>No security issues found.</td></tr>")
                        else:
                            f.write(f"<tr><td>Bandit</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} security issues found.</td></tr>")
                    except json.JSONDecodeError as e:
                        f.write(f"<tr><td>Bandit</td><td class='warning center'>Warning</td><td class='center'>N/A</td><td>Failed to parse Bandit results: {e}</td></tr>")
                elif analyzer_name == "mypy":
                    if "Success" in result:
                        f.write(f"<tr><td>MyPy</td><td class='good center'>Good</td><td class='center'>0</td><td>No type issues found.</td></tr>")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(f"<tr><td>MyPy</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} type issues found.</td></tr>")
                elif analyzer_name == "pylint":
                    issue_count = sum(1 for line in result.splitlines() if "rated at" not in line and line.strip())
                    if issue_count == 0:
                        f.write(f"<tr><td>Pylint</td><td class='good center'>Good</td><td class='center'>0</td><td>No issues found.</td></tr>")
                    else:
                        f.write(f"<tr><td>Pylint</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} issues found.</td></tr>")
                elif analyzer_name == "flake8":
                    if result.strip() == "":
                        f.write(f"<tr><td>Flake8</td><td class='good center'>Good</td><td class='center'>0</td><td>No issues found.</td></tr>")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(f"<tr><td>Flake8</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} issues found.</td></tr>")
            f.write("</table></div>")

            # Detailed Results Section
            for analyzer_name, result in self.analysis_results.items():
                f.write(f"<h2>{analyzer_name.capitalize()} Results</h2>")
                f.write("<pre class='issue'>")
                if analyzer_name == "bandit":
                    try:
                        bandit_result = json.loads(result)
                        f.write(f"Total Issues: {len(bandit_result.get('results', []))}<br>")
                        metrics = bandit_result.get("metrics", {})
                        f.write("Key Metrics:<br>")
                        for key, value in metrics.get("_totals", {}).items():
                            f.write(f"{key.replace('_', ' ').title()}: {value}<br>")
                    except json.JSONDecodeError:
                        f.write(result)
                else:
                    f.write(result)
                f.write("</pre>")

            f.write("""
            </body>
            </html>
            """)
