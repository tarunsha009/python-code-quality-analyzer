import json

from reports.report import Report


class MarkdownReport(Report):
    def generate(self, output_file):
        with open(output_file, "w") as f:
            f.write(f"# Code Quality Report\n\n")

            # Summary Section
            f.write("## Summary\n\n")
            for analyzer_name, result in self.analysis_results.items():
                if analyzer_name == "bandit":
                    try:
                        bandit_result = json.loads(result)
                        issue_count = len(bandit_result.get("results", []))
                        if issue_count == 0:
                            f.write(f"### Bandit\n- **Status:** Good\n- **Issues:** 0\n- **Comments:** No security issues found.\n\n")
                        else:
                            f.write(f"### Bandit\n- **Status:** Issues\n- **Issues:** {issue_count}\n- **Comments:** {issue_count} security issues found.\n\n")
                    except json.JSONDecodeError as e:
                        f.write(f"### Bandit\n- **Status:** Warning\n- **Issues:** N/A\n- **Comments:** Failed to parse Bandit results: {e}\n\n")
                elif analyzer_name == "mypy":
                    if "Success" in result:
                        f.write(f"### MyPy\n- **Status:** Good\n- **Issues:** 0\n- **Comments:** No type issues found.\n\n")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(f"### MyPy\n- **Status:** Issues\n- **Issues:** {issue_count}\n- **Comments:** {issue_count} type issues found.\n\n")
                elif analyzer_name == "pylint":
                    issue_count = sum(1 for line in result.splitlines() if "rated at" not in line and line.strip())
                    if issue_count == 0:
                        f.write(f"### Pylint\n- **Status:** Good\n- **Issues:** 0\n- **Comments:** No issues found.\n\n")
                    else:
                        f.write(f"### Pylint\n- **Status:** Issues\n- **Issues:** {issue_count}\n- **Comments:** {issue_count} issues found.\n\n")
                elif analyzer_name == "flake8":
                    if result.strip() == "":
                        f.write(f"### Flake8\n- **Status:** Good\n- **Issues:** 0\n- **Comments:** No issues found.\n\n")
                    else:
                        issue_count = len(result.splitlines())
                        f.write(f"### Flake8\n- **Status:** Issues\n- **Issues:** {issue_count}\n- **Comments:** {issue_count} issues found.\n\n")

            # Detailed Results Section
            f.write("## Detailed Results\n\n")
            for analyzer_name, result in self.analysis_results.items():
                f.write(f"### {analyzer_name.capitalize()} Results\n\n")
                if analyzer_name == "bandit":
                    try:
                        bandit_result = json.loads(result)
                        f.write(f"**Total Issues:** {len(bandit_result.get('results', []))}\n\n")
                        metrics = bandit_result.get("metrics", {})
                        f.write("**Key Metrics:**\n\n")
                        for key, value in metrics.get("_totals", {}).items():
                            f.write(f"- {key.replace('_', ' ').title()}: {value}\n")
                    except json.JSONDecodeError:
                        f.write(result)
                else:
                    f.write("```\n" + result + "\n```\n")

