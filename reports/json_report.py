import json
from reports.report import Report


class JSONReport(Report):

    def generate(self, output_file):
        combined_results = {}

        for analyzer_name, result in self.analysis_results.items():
            combined_results[analyzer_name] = result

        with open(output_file, 'w') as file:
            json.dump(combined_results, file, indent=4)