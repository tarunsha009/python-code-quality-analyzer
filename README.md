# Python Code Quality Analyzer

This project is a Python code quality analyzer designed to analyze Python scripts using popular tools like Pylint and Flake8. The tool generates reports in various formats (e.g., HTML, JSON) and can be easily extended with additional analyzers or enhanced with AI capabilities in the future.

## Features

- **Pylint Analyzer:** Analyze Python code for coding standard violations and potential issues.
- **Flake8 Analyzer:** Check Python code for style guide enforcement and programming errors.
- **Report Generation:** Generate reports in HTML and JSON formats.
- **Modular Design:** Easily extendable with new analyzers or report formats.

## Project Structure

```
.
└── code_quality_analyzer/
    ├── analyzers/
    │   ├── __init__.py
    │   ├── pylint_analyzer.py
    │   ├── flake8_analyzer.py
    ├── reports/
    │   ├── __init__.py
    │   ├── html_report.py
    │   ├── json_report.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_analyzers.py
    ├── utils/
    │   ├── __init__.py
    │   ├── config_loader.py
    ├── config.yaml
    ├── requirements.txt
    ├── example.py
    └── main.py
```

## Getting Started

### Prerequisites

- Python 3.x
- Pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/python-code-quality-analyzer.git
   cd python-code-quality-analyzer
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Run the Analyzer:**

   The `main.py` script serves as the entry point for running the code quality analyzer:

   ```bash
   python main.py
   ```

   This will analyze the `example.py` file using Pylint and Flake8, and generate reports in both HTML and JSON formats.

2. **View Reports:**

   - The HTML report will be generated as `pylint_report.html`.
   - The JSON report will be generated as `combined_report.json`.

### Extending the Project

- **Adding New Analyzers:** You can add new analyzers by creating additional classes in the `analyzers/` directory and integrating them into the `main.py` script.
- **Customizing Reports:** To add new report formats, create new classes in the `reports/` directory and modify the report generation section in `main.py`.

### Testing

- **Run Unit Tests:**

   The project includes basic unit tests located in the `tests/` directory. Run them using the following command:

   ```bash
   python -m unittest discover -s tests
   ```

### Future Enhancements

- **AI Integration:** Future versions of this project may include AI capabilities to enhance the code quality analysis with more intelligent insights and suggestions.
- **More Analyzers:** Adding additional code analysis tools (e.g., Bandit for security checks, MyPy for type checking) to cover more aspects of code quality.

### Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Make sure to follow the coding standards and write unit tests for new features.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Acknowledgments

- This project uses Pylint and Flake8, both of which are essential tools for Python code quality analysis.
- Inspired by the need for a modular and extendable code quality analyzer that can grow with the needs of developers.

---