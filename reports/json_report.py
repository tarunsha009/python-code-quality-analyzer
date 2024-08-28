import json
from reports.report import Report


class JSONReport(Report):

    def generate(self, output_file):
        with open(output_file, "w") as f:
            json.dump(self.pylint_data, f, indent=4)
            json.dump(self.flake8_data, f, indent=4)


# if __name__ == "__main__":
#     report = JSONReport({"example": "data"})
#     report.generate("report.json")
