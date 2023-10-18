import os


def sudo(command, password=None):
    """
    Execute sudo commands non-interactively in the shell.
    If the password is not specified by argument, the function
    reads the password from the environment variable
    `EXUSE_SUDO_PASSWORD`, and raises `ValueError` if the environment
    variable is also not specified.
    """
    if password is None:
        password = os.environ.get("EXUSE_SUDO_PASSWORD")
    if password is None:
        raise ValueError("Environment variable EXUSE_SUDO_PASSWORD not found")
    return f"echo {password} | sudo -S -p '' {command}"
