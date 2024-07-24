from helpers import run_powershell_command

def sync_date_time():
    run_powershell_command("net stop w32time")
    run_powershell_command("w32tm /unregister")
    run_powershell_command("w32tm /register")
    run_powershell_command("net start w32time")
    run_powershell_command("w32tm /resync")