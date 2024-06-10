import subprocess
import os


def create_virtual_env(env_name="venv"):
    # Create a virtual environment
    subprocess.run(["python", "-m", "venv", env_name])
    print(f"Virtual environment '{env_name}' created.")


def activate_virtual_env(env_name="venv"):
    # Activate the virtual environment
    activate_script = os.path.join(env_name, "Scripts", "activate.bat")
    subprocess.run(["cmd", "/k", activate_script])
    print(f"Virtual environment '{env_name}' activated.")


def install_requirements(env_name="venv", requirements_file="requirements.txt"):
    # Install the requirements
    pip_path = os.path.join(env_name, "Scripts", "pip.exe")
    subprocess.run([pip_path, "install", "-r", requirements_file])
    print(f"Requirements from '{requirements_file}' installed.")


if __name__ == "__main__":
    env_name = "venv"
    requirements_file = "requirements.txt"

    create_virtual_env(env_name)
    activate_virtual_env(env_name)
    install_requirements(env_name, requirements_file)