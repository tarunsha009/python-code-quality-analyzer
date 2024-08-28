from fpdf import FPDF
import json

from reports.report import Report


class PDFReport(Report):
    def generate(self, output_file):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Title
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(0, 10, "Code Quality Report", ln=True, align="C")
        pdf.ln(10)

        # Summary Section
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(0, 10, "Summary", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        for analyzer_name, result in self.analysis_results.items():
            if analyzer_name == "bandit":
                try:
                    bandit_result = json.loads(result)
                    issue_count = len(bandit_result.get("results", []))
                    if issue_count == 0:
                        pdf.cell(0, 10, "Bandit: No security issues found.", ln=True)
                    else:
                        pdf.cell(0, 10, f"Bandit: {issue_count} security issues found.", ln=True)
                except json.JSONDecodeError as e:
                    pdf.cell(0, 10, f"Bandit: Failed to parse Bandit results: {e}", ln=True)
            elif analyzer_name == "mypy":
                if "Success" in result:
                    pdf.cell(0, 10, "MyPy: No type issues found.", ln=True)
                else:
                    issue_count = len(result.splitlines())
                    pdf.cell(0, 10, f"MyPy: {issue_count} type issues found.", ln=True)
            elif analyzer_name == "pylint":
                issue_count = sum(1 for line in result.splitlines() if "rated at" not in line and line.strip())
                if issue_count == 0:
                    pdf.cell(0, 10, "Pylint: No issues found.", ln=True)
                else:
                    pdf.cell(0, 10, f"Pylint: {issue_count} issues found.", ln=True)
            elif analyzer_name == "flake8":
                if result.strip() == "":
                    pdf.cell(0, 10, "Flake8: No issues found.", ln=True)
                else:
                    issue_count = len(result.splitlines())
                    pdf.cell(0, 10, f"Flake8: {issue_count} issues found.", ln=True)
            pdf.ln(5)

        # Detailed Results Section
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(0, 10, "Detailed Results", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        for analyzer_name, result in self.analysis_results.items():
            pdf.set_font("Arial", size=12, style="B")
            pdf.cell(0, 10, f"{analyzer_name.capitalize()} Results", ln=True)
            pdf.set_font("Arial", size=12)
            if analyzer_name == "bandit":
                try:
                    bandit_result = json.loads(result)
                    pdf.cell(0, 10, f"Total Issues: {len(bandit_result.get('results', []))}", ln=True)
                    metrics = bandit_result.get("metrics", {})
                    pdf.cell(0, 10, "Key Metrics:", ln=True)
                    for key, value in metrics.get("_totals", {}).items():
                        pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
                except json.JSONDecodeError:
                    pdf.multi_cell(0, 10, result)
            else:
                pdf.multi_cell(0, 10, result)
            pdf.ln(5)

        pdf.output(output_file)

