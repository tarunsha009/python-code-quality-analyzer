import json


class JSONReport:
    def __init__(self, data):
        self.data = data

    def generate(self, output_file):
        with open(output_file, "w") as f:
            json.dump(self.data, f, indent=4)


if __name__ == "__main__":
    report = JSONReport({"example": "data"})
    report.generate("report.json")
