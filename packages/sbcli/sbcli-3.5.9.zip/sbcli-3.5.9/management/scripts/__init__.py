import logging
import os
import subprocess

from management import shell_utils

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger()


def __run_script(args: list):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, text=True, stderr=subprocess.STDOUT)
    while True:
        result = process.poll()
        if result is not None:
            break
        output = process.stdout.readline()
        if output:
            logger.debug(output.strip())

    return process.returncode


def install_deps():
    return __run_script(['bash', '-x', os.path.join(DIR_PATH, 'install_deps.sh')])


def deploy_stack(CLI_PASS, DEV_IP):
    return __run_script(['sudo', 'bash', '-x', os.path.join(DIR_PATH, 'deploy_stack.sh'), DIR_PATH, CLI_PASS, DEV_IP])


def deploy_cleaner():
    return __run_script(['sudo', 'bash', '-x', os.path.join(DIR_PATH, 'clean_local_storage_deploy.sh')])


def set_db_config(DEV_IP):
    return __run_script(['bash', os.path.join(DIR_PATH, 'set_db_config.sh'), DEV_IP])


def set_db_config_single():
    return __run_script(['bash', os.path.join(DIR_PATH, 'db_config_single.sh')])


def set_db_config_double():
    return __run_script(['bash', os.path.join(DIR_PATH, 'db_config_double.sh')])
