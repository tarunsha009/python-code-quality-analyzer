import yaml
import logging


def load_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded from {config_path}")
        return config

    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        print(f"Error: Configuration file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {config_path}. YAML error: {e}")
        print(f"Error: Could not parse configuration file: {config_path}. Please check the file format.")
        return None
    except Exception as e:
        logging.error(f"Unexpected error loading configuration: {e}")
        print(f"Error: Unexpected error loading configuration: {e}")
        return None
