import logging.config
import os
import pathlib


def logging_config():
    working_dir = pathlib.Path().resolve()
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
