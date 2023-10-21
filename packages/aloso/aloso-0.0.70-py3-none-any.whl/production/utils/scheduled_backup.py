from output.shell.configs_shell import ConfigsShell
from output.shell.data_backup_shell import BackupShell

if __name__ == "__main__":
    BackupShell.schedule_backup(password=ConfigsShell.get_value('backup_password'))
