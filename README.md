# Python Code Quality Analyzer

This project is a Python code quality analyzer designed to analyze Python scripts using popular tools like Pylint, Flake8, Bandit, MyPy, Safety, Isort, and Vulture. The tool generates reports in various formats (e.g., HTML, JSON, Markdown, PDF) and is designed to be easily extendable with additional analyzers or enhancements, including AI capabilities in the future.

## Features

- **Pylint Analyzer:** Analyze Python code for coding standard violations and potential issues, with customizable rules.
- **Flake8 Analyzer:** Check Python code for style guide enforcement and programming errors.
- **Bandit Analyzer:** Identify security issues in Python code.
- **MyPy Analyzer:** Perform static type checking.
- **Safety Analyzer:** Check for known security vulnerabilities in dependencies.
- **Isort Analyzer:** Ensure consistent import order.
- **Vulture Analyzer:** Detect unused code.
- **Report Generation:** Generate reports in multiple formats, including HTML, JSON, Markdown, and PDF.
- **Configurable Rules:** Customize which rules to disable via a configuration file.
- **Parallel Processing:** Run analyses concurrently for improved performance.
- **Modular Design:** Easily extendable with new analyzers or report formats.

## Project Structure

```
.
└── code_quality_analyzer/
    ├── analyzers/
    │   ├── __init__.py
    │   ├── pylint_analyzer.py
    │   ├── flake8_analyzer.py
    │   ├── bandit_analyzer.py
    │   ├── mypy_analyzer.py
    │   ├── safety_analyzer.py
    │   ├── isort_analyzer.py
    │   ├── vulture_analyzer.py
    ├── reports/
    │   ├── __init__.py
    │   ├── html_report.py
    │   ├── json_report.py
    │   ├── markdown_report.py
    │   ├── pdf_report.py
    ├── utils/
    │   ├── __init__.py
    │   ├── config_loader.py
    │   ├── logger.py
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

### Configuration

1. **Edit the `config.yaml` file:**

   - Specify the path to file or directory
   - Specify the report type
   - Customize the analyzers to enable/disable.
   - Specify which Pylint rules to disable, if any.
   - Set up logging preferences and report generation formats.

   Example `config.yaml`:

   ```yaml
   input:
      path: "C:\\Path\\To\\Your\\PythonFileOrDirectory"
      report_type: "html"  # Options: html, json, markdown, pdf
   
   logging:
     level: DEBUG
     file: code_quality_analyzer.log

   report:
     default_type: html
     output_directory: results

   analyzers:
     pylint: true
     flake8: true
     bandit: true
     mypy: true
     safety: true
     isort: true
     vulture: true

   pylint:
     disable_rules:
       - logging-fstring-interpolation
   ```

### Usage

1. **Run the Analyzer:**

   The `main.py` script serves as the entry point for running the code quality analyzer:

   ```bash
   python main.py
   ```

   This will analyze the Python files in the specified directory using the configured analyzers and generate reports in the chosen formats.

2. **View Reports:**

   - Reports will be generated in the specified output directory (default: `results/`).
   - Reports can be viewed in HTML, JSON, Markdown, or PDF formats depending on the configuration.

### Extending the Project

- **Adding New Analyzers:** To add new analyzers, create additional classes in the `analyzers/` directory and integrate them into the `main.py` script.
- **Customizing Reports:** To add new report formats, create new classes in the `reports/` directory and modify the report generation logic in `main.py`.

### Future Enhancements

- **AI Integration:** Future versions of this project may include AI capabilities to enhance the code quality analysis with more intelligent insights and suggestions.
- **Plugin System:** Develop a plugin system to make it easier for users to add their own analyzers or reporting formats without modifying the core codebase.
- **User Interface:** Consider building a simple GUI to make the tool more accessible to non-developers.

### Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Make sure to follow the coding standards and write unit tests for new features.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Acknowledgments

- This project uses Pylint, Flake8, Bandit, MyPy, Safety, Isort, and Vulture, all of which are essential tools for Python code quality analysis.
- Inspired by the need for a modular and extendable code quality analyzer that can grow with the needs of developers.

---