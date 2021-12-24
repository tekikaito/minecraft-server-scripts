import commons
import argparse
import logger
import subprocess
import time
import os


__start_time__ = int(time.time())

log = logger.get_logger(
    'delete-old-backups',
    {
        'USE_CONSOLE': 'true',
        'USE_FILE': 'true',
        'USE_DISCORD': 'false',
        'FILE_NAME': f'{commons.LOGS_PATH}/backup-removal.log',
        'MAX_BYTES': int(commons.get_env_or_fail('LOG_MAX_BYTES')),
        'BACKUP_COUNT': 2,
        'ENCODING': 'UTF-8'
    }
)


def parse_params_dict():
    parser = argparse.ArgumentParser()
    parser.add_argument('max_age', type=int)
    return parser.parse_args()


def get_backup_file_names():
    print(list(os.scandir(commons.BACKUPS_PATH)))
    return os.scandir(commons.BACKUPS_PATH)


def get_time_stamp(dir_entry: os.DirEntry):
    file_path = dir_entry.path
    time_stamp = file_path[len(commons.FILE_NAME_ROOT):len(
        file_path) - len(commons.FILE_ENDING)]
    return int(time_stamp)


def expired(timestamp: int, max_age: int):
    return timestamp < __start_time__ - max_age


def get_expired_dir_entries(max_age: int):
    def file_expired(filename: os.DirEntry):
        return expired(get_time_stamp(filename), max_age)
    return filter(file_expired, get_backup_file_names())


def unlink_file(filename: str):
    log.debug(f'removing {filename} ...')
    subprocess.call(f'rm -f {filename}', shell=True)


def delete_old_backups(max_age: int):
    display_age = f'{max_age / float(60) if max_age >= 60 else max_age} {"minute(s)" if max_age >= 60 else "second(s)"}'
    log.info(f'removing backups older than {display_age} ...')

    global __start_time__
    __start_time__ = int(time.time())
    expired_entries = get_expired_dir_entries(max_age)

    backups_unlinked = 0
    for entry in expired_entries:
        unlink_file(entry.path)
        backups_unlinked += 1
        yield entry.path

    if backups_unlinked == 0:
        log.debug('no files removed')

#  ____
# < hi >
#  ----
#         \   ^__^
#          \  (oo)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||


if __name__ == '__main__':
    params = parse_params_dict()
    deleted_backups = list(delete_old_backups(params.max_age))
