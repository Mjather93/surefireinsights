import os
import pathlib
import logging.config
import subprocess
import yaml
import logging_config


def load_conf_file(file_path):
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
        return config


logging_config.logging_config()
working_dir = pathlib.Path().resolve()
config_file = str(working_dir) + "/config/conf.yaml"
scripts = load_conf_file(file_path=config_file)
