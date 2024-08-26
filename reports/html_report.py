class HTMLReport:
    def __init__(self, data):
        self.data = data

    def generate(self, output_file):
        with open(output_file, "w") as f:
            f.write("<html><body>")
            f.write("<h1>Code Quality Report</h1>")
            f.write("<pre>")
            f.write(self.data)
            f.write("</pre>")
            f.write("</body></html>")


if __name__ == "__main__":
    report = HTMLReport("Example report data")
    report.generate("report.html")
