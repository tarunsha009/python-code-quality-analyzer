class HTMLReport:
    def __init__(self, pylint_data, flake_data):
        self.pylint_data = pylint_data
        self.flake_data = flake_data

    def generate(self, output_file):
        with open(output_file, "w") as f:
            f.write("<html><body>")
            f.write("<h1>Code Quality Report</h1>")

            # Pylint section
            f.write("<h2>Pylint Results</h2>")
            f.write("<pre>")
            f.write(self.pylint_data)
            f.write("</pre>")

            # Flake8 section
            f.write("<h2>Flake8 Results</h2>")
            f.write("<pre>")
            f.write(self.flake_data)
            f.write("</pre>")

            f.write("</body></html>")


# if __name__ == "__main__":
#     report = HTMLReport("Example report data")
#     report.generate("report.html")
