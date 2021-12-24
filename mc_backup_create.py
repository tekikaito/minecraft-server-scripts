#!/bin/python3

import subprocess
import time
import signal
import logger
import commons

log = logger.get_logger(
    'create-backups',
    {
        'USE_CONSOLE': 'true',
        'USE_FILE': 'true',
        'USE_DISCORD': 'false',
        'FILE_NAME': f'{commons.LOGS_PATH}/backup-creation.log',
        'MAX_BYTES': int(commons.get_env_or_fail('LOG_MAX_BYTES')),
        'BACKUP_COUNT': 2,
        'ENCODING': 'UTF-8'
    }
)


def get_sigint_handler(target_file):
    def handler(signal, frame):
        log.error('backup creation interrupted')
        log.debug(f'removing unfinished backup target -> {target_file}')
        subprocess.call(f'rm -f {target_file}', shell=True)
        exit(0)
    return handler


def create_backup(backuped_dir, target_file, attach_interrupt_handler=False):
    if attach_interrupt_handler:
        signal.signal(signal.SIGINT, get_sigint_handler(target_file))
    command = f'tar -cvpzf {target_file} --exclude="{backuped_dir}/plugins/dynmap/web/tiles/world" {backuped_dir}'
    log.debug(f'BACKUPED_FOLDER: {backuped_dir}')
    log.debug(command)
    subprocess.call(command, shell=True)
    log.info(f'successfully created backup {target_file}')


def create_default_backup(attach_interrupt_handler=False):
    TIME_NOW = int(time.time())
    TARGET_FILE = f'{commons.FILE_NAME_ROOT}{TIME_NOW}{commons.FILE_ENDING}'
    create_backup(
        commons.DATA_DIRECTORY,
        TARGET_FILE,
        attach_interrupt_handler
    )
    return TARGET_FILE


if __name__ == '__main__':
    create_default_backup(attach_interrupt_handler=True)
