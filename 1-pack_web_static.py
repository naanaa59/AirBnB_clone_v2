#!/usr/bin/python3
"""
    This is a Fabric script that generates a .tgz archive
    from content of web_static folder
"""
from fabric.api import local
import time


def do_pack():
    """
        adds all files in web_static folder to final archive
        store them in a folder named versions
        the name of the folder is:
            web_static_<year><month><day><hour><minute><second>.tgz
    """
    try:
        local("mkdir -p versions")
        source_path = "web_static/"
        archive = "versions/web_static_{}.tgz".format(
                time.strftime("%Y%m%d%H%M%S"))
        local("tar -czvf {} {}".format(archive, source_path))
        return archive

    except Exception as e:
        return None
