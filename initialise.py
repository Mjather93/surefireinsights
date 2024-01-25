import os
import pathlib
import logging.config
import subprocess
import yaml


def load_conf_file(file_path):
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
        return config


working_dir = pathlib.Path().resolve()
config_file = str(working_dir) + "/config/conf.yaml"
log_config_file = str(working_dir) + "/config/logging.conf"
logfile = str(working_dir) + '/logs/system.log'
logdir = os.path.dirname(logfile)
if not pathlib.Path(logdir).exists():
    try:
        os.makedirs(logdir)
        print("Created directory '%s'" % logdir)
    except OSError as error:
        logging.critical("Exception occurred", exc_info=True)
log = open(logfile, "a")
log.close()
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False,
                          defaults={'logfilename': logfile.replace("\\", "/")})
logging.info('test.py has initialised.')
scripts = load_conf_file(file_path=config_file)

# If it doesn't already exist, create the sqlite database
subprocess.run(["python", "create_sqlite_db.py"])
