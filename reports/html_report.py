import json
from reports.report import Report


class HTMLReport(Report):
    def generate(self, output_file):
        # summary = self.extract_summary()

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
                        bandit_result = json.loads(result)
                        issue_count = len(bandit_result.get("results", []))
                        if issue_count == 0:
                            f.write(
                                f"<tr><td>Bandit</td><td class='good center'>Good</td><td class='center'>0</td><td>No security issues found.</td></tr>")
                        else:
                            f.write(
                                f"<tr><td>Bandit</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} security issues found.</td></tr>")
                    except json.JSONDecodeError as e:
                        f.write(
                            f"<tr><td>Bandit</td><td class='warning center'>Warning</td><td class='center'>N/A</td><td>Failed to parse Bandit results: {e}</td></tr>")

                elif analyzer_name == "mypy":
                    if "Success" in result:
                        f.write(
                            f"<tr><td>MyPy</td><td class='good center'>Good</td><td class='center'>0</td><td>No type issues found.</td></tr>")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(
                            f"<tr><td>MyPy</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} type issues found.</td></tr>")

                elif analyzer_name == "pylint":
                    issue_count = sum(1 for line in result.splitlines() if "rated at" not in line and line.strip())
                    if issue_count == 0:
                        f.write(
                            f"<tr><td>Pylint</td><td class='good center'>Good</td><td class='center'>0</td><td>No issues found.</td></tr>")
                    else:
                        f.write(
                            f"<tr><td>Pylint</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} issues found.</td></tr>")

                elif analyzer_name == "flake8":
                    if result.strip() == "":
                        f.write(
                            f"<tr><td>Flake8</td><td class='good center'>Good</td><td class='center'>0</td><td>No issues found.</td></tr>")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(
                            f"<tr><td>Flake8</td><td class='bad center'>Issues</td><td class='center'>{issue_count}</td><td>{issue_count} issues found.</td></tr>")

                elif analyzer_name == "safety":
                    try:
                        # safety_result = json.loads(result)
                        safety_result = result
                        if safety_result == 'No requirements.txt found.':
                            f.write(
                                f"<tr><td>Safety</td><td class='warning center'>Warning</td><td class='center'>No Scan Performed</td><td>{safety_result}</td></tr>")
                        else:
                            vulnerabilities = len(safety_result.get("vulnerabilities", []))
                            ignored_vulnerabilities = len(safety_result.get("ignored_vulnerabilities", []))
                            if vulnerabilities == 0 and ignored_vulnerabilities == 0:
                                f.write(
                                    f"<tr><td>Safety</td><td class='good center'>Good</td><td class='center'>0</td><td>No vulnerabilities found.</td></tr>")
                            elif vulnerabilities > 0:
                                f.write(
                                    f"<tr><td>Safety</td><td class='bad center'>Issues</td><td class='center'>{vulnerabilities}</td><td>{vulnerabilities} vulnerabilities found.</td></tr>")
                            else:
                                f.write(
                                    f"<tr><td>Safety</td><td class='warning center'>Warning</td><td class='center'>{ignored_vulnerabilities}</td><td>{ignored_vulnerabilities} vulnerabilities ignored.</td></tr>")
                    except json.JSONDecodeError as e:
                        f.write(
                            f"<tr><td>Safety</td><td class='warning center'>Warning</td><td class='center'>N/A</td><td>Failed to parse Safety results: {e}</td></tr>")

                elif analyzer_name == "isort":
                    if "No issues found" in result:
                        f.write(
                            f"<tr><td>Isort</td><td class='good center'>Good</td><td class='center'>0</td><td>Imports are correctly sorted.</td></tr>")
                    else:
                        f.write(
                            f"<tr><td>Isort</td><td class='bad center'>Issues</td><td class='center'>Issues found</td><td>Issues found in import sorting.</td></tr>")

                elif analyzer_name == "vulture":
                    total_issues = sum(1 for result in self.analysis_results.values() if result.strip())

                    if total_issues == 0:
                        f.write(
                            f"<tr><td>Vulture</td><td class='good center'>Good</td><td class='center'>0</td><td>No dead code found.</td></tr>")
                    else:
                        f.write(
                            f"<tr><td>Vulture</td><td class='bad center'>Issues</td><td class='center'>{total_issues}</td><td>Potential dead code found.</td></tr>")

                    f.write("<h2>Vulture Results</h2>")

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

                elif analyzer_name == "safety":
                    try:
                        safety_result = result
                        if safety_result == 'No requirements.txt found.':
                            f.write(f"No Scan Performed on Packages.<br>")
                        else:
                            f.write(f"Scanned Packages: {result.get('report_meta', {}).get('packages_found', 'N/A')}<br>")
                            f.write(
                                f"Vulnerabilities Found: {result.get('report_meta', {}).get('vulnerabilities_found', 'N/A')}<br>")
                            f.write(
                                f"Vulnerabilities Ignored: {result.get('report_meta', {}).get('vulnerabilities_ignored', 'N/A')}<br>")
                            f.write(
                                f"Remediations Recommended: {result.get('report_meta', {}).get('remediations_recommended', 'N/A')}<br>")

                            vulnerabilities = safety_result.get("vulnerabilities", [])
                            for vuln in vulnerabilities:
                                f.write(
                                    f"<strong>Package:</strong> {vuln['package_name']} ({vuln['analyzed_version']})<br>")
                                f.write(f"<strong>Vulnerability ID:</strong> {vuln['vulnerability_id']}<br>")
                                f.write(f"<strong>Description:</strong> {vuln['advisory']}<br>")
                                f.write(f"<strong>CVE:</strong> {vuln['CVE']}<br>")
                                f.write(f"<strong>More Info:</strong> <a href='{vuln['more_info_url']}'>Link</a><br><br>")
                            if safety_result.get('ignored_vulnerabilities', []):
                                f.write("<h3>Ignored Vulnerabilities:</h3>")
                                for ignored in safety_result['ignored_vulnerabilities']:
                                    f.write(f"Package: {ignored['package_name']} - Reason: {ignored['ignored_reason']}<br>")
                                    f.write(
                                        f"<strong>More Info:</strong> <a href='{ignored['more_info_url']}'>Link</a><br><br>")
                    except json.JSONDecodeError:
                        f.write(result)

                elif analyzer_name == "isort":
                    if "No issues found" in result:
                        f.write(
                            f"<tr><td>Isort</td><td class='good center'>Good</td><td class='center'>0</td><td>Imports are correctly sorted.</td></tr>")
                    else:
                        f.write(
                            f"<tr><td>Isort</td><td class='bad center'>Issues</td><td class='center'>Issues found</td><td>Issues found in import sorting.</td></tr>")

                        # Displaying detailed diff in a more readable format
                        f.write(f"<h2>Isort Results</h2>")
                        f.write("<pre style='background-color: #f9f9f9; padding: 10px; border-radius: 5px;'>")

                        # Splitting the diff output into lines and formatting each line
                        for line in result.splitlines():
                            if line.startswith("---") or line.startswith("+++"):
                                f.write(f"<span style='color: #005cc5;'>{line}</span><br>")
                            elif line.startswith("-"):
                                f.write(f"<span style='color: red;'>{line}</span><br>")
                            elif line.startswith("+"):
                                f.write(f"<span style='color: green;'>{line}</span><br>")
                            else:
                                f.write(f"{line}<br>")

                        f.write("</pre>")

                elif analyzer_name == "vulture":
                    if result:
                        f.write(f"<h3>{analyzer_name}</h3>")
                        f.write("<pre class='issue'>")
                        # Split the string by new lines and write each line to the HTML
                        for line in result.splitlines():
                            f.write(f"{line}<br>")
                        f.write("</pre>")

                else:
                    f.write(result)
                f.write("</pre>")

            f.write("""
            </body>
            </html>
            """)
