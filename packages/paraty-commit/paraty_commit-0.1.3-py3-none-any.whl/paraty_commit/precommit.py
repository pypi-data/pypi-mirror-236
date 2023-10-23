import os
import pkg_resources
import shutil
import subprocess
from colorama import Fore, init, Style

FILES_TO_COPY = ['.pre-commit-config.yaml', 'pylintrc']

def main():
    init(autoreset=True)

    print(Style.BRIGHT + Fore.GREEN + "Installing Paraty Pre-Commit...")
    project_path = os.getcwd()
    package_name = 'paraty_commit'
    package_path = pkg_resources.resource_filename(package_name, '')

    files = os.listdir(package_path)
    files = [file for file in files if file in FILES_TO_COPY]
    files = [file for file in files if os.path.isfile(os.path.join(package_path, file))]

    print(Style.BRIGHT + Fore.GREEN + f"Package Path: {package_path}")
    print(Style.BRIGHT + Fore.GREEN + f"Project Path: {project_path}")

    for file in files:
        file_name_path = os.path.join(package_path, file)
        file_name_project_path = os.path.join(project_path, file)
        shutil.copy(file_name_path, file_name_project_path)
        print(Fore.GREEN + f"Added file: {file}")

    execute_command("pip install pre-commit==2.9.2")
    execute_command("git add .pre-commit-config.yaml")
    execute_command("pre-commit autoupdate --bleeding-edge")
    execute_command("pre-commit install")
    execute_command("pip install pylint")

    print(Style.BRIGHT + Fore.GREEN + "Paraty Pre-Commit Installed!!")


def execute_command(comando):
    print(Style.BRIGHT + Fore.GREEN + f">> {comando}")
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida_stdout, salida_stderr = proceso.communicate()
    codigo_salida = proceso.returncode
    if salida_stderr:
        print(salida_stderr.decode('utf-8'))
        print("<<<<<<<<<<<<<<<<<<<<<<<")
    if salida_stdout:
        print(salida_stdout.decode('utf-8'))
        print("<<<<<<<<<<<<<<<<<<<<<<<")

    if proceso.returncode != 0:
        print(Style.BRIGHT + Fore.RED + "Installation Aborted!")
        exit(-1)

if __name__ == '__main__':
   main()