#!/usr/bin/python3
"""
This script that generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo,
using the function do_pack.
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """Ths function generates a tgz archive"""
    try:
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        if not isdir("versions"):
            local("mkdir -p versions")
        file_name = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {file_name} web_static")
        return file_name
    except Exceptio as e:
        return None
