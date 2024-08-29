"""
Module for analyzing Python files and directories using various analyzers.
"""

import logging
import os
from typing import Dict


def analyze_file(file_path: str, analyzers: Dict[str, object]) -> Dict[str, str]:
    """
    Analyzes a single Python file using the provided analyzers.

    Args:
        file_path (str): Path to the Python file to analyze.
        analyzers (dict): Dictionary of analyzer instances.

    Returns:
        dict: A dictionary containing the results of each analyzer.
    """
    results = {}
    for name, analyzer in analyzers.items():
        try:
            logging.info(f"Running {name} analysis on {file_path}")
            results[name] = analyzer.analyze(file_path)
        except SystemExit as e:
            logging.warning(
                f"{name} exited with code {e.code} for file {file_path}"
            )
        except FileNotFoundError as e:
            logging.error(
                f"{name} failed on {file_path}: File not found - {e}"
            )
            results[name] = f"Error during {name} analysis: File not found"
        except PermissionError as e:
            logging.error(
                f"{name} failed on {file_path}: Permission denied - {e}"
            )
            results[name] = f"Error during {name} analysis: Permission denied"
        except Exception as e:
            logging.error(
                f"Unexpected error during {name} analysis of {file_path}: {e}"
            )
            results[name] = f"Unexpected error during {name} analysis: {e}"

    return results


def analyze_directory(directory: str, analyzers: Dict[str, object]) -> Dict[str, Dict[str, str]]:
    """
    Analyzes all Python files in the given directory and its subdirectories.

    Args:
        directory (str): Path to the directory to analyze.
        analyzers (dict): Dictionary of analyzer instances.

    Returns:
        dict: A dictionary containing the results of each
        analyzer for each file.
    """
    ignore_dirs = {'.venv', '.idea', '.git', '__pycache__', 'venv'}
    analysis_results = {}

    for root, dirs, files in os.walk(directory):
        # Filter out directories to ignore
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                analysis_results[file_path] = analyze_file(file_path, analyzers)

    return analysis_results
