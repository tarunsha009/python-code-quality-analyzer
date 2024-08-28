from abc import ABC, abstractmethod


class Report(ABC):

    def __init__(self, analysis_results):
        self.analysis_results = analysis_results

    @abstractmethod
    def generate(self, output_file):
        pass

    def extract_summary(self):
        summary = {}
        for analyzer_name, result in self.analysis_results.items():
            issue_count = result.count("\n")
            summary[analyzer_name] = issue_count
        return summary