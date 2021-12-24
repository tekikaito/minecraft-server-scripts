import os


def get_env_or_fail(var_name: str):
    try:
        return os.environ[var_name]
    except:
        print(f'[-] failed to read environment variable "{var_name}"')


DATA_DIRECTORY = '/app/data'
BACKUPS_PATH = '/app/backups'
LOGS_PATH = '/app/logs'
FILE_ENDING = get_env_or_fail('MINECRAFT_BACKUP_FILE_ENDING')
FILE_NAME_ROOT = f'{BACKUPS_PATH}/backup-'
