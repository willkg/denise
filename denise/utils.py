import subprocess


def call_command(cmd, verbose=False):
    if verbose:
        print cmd
    subprocess.call(cmd)


def truthiness(s):
    """Returns a boolean from a string"""
    try:
        return str(s).lower() in ['true', 't', '1']
    except (TypeError, ValueError, UnicodeEncodeError):
        return False
