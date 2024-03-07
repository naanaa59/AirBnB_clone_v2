#!/usr/bin/python3
"""
    This is a Fabric script that generates a .tgz archive
    from content of web_static folder
    It deploys the archive to web servers
"""
from fabric.api import *
import time
import os

env.hosts = ["54.158.203.28", "52.91.156.191"]
env.user = "ubuntu"


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


def do_deploy(archive_path):
    """
        Deploys and distributes an archive to web servers
    """

    if os.path.exists(archive_path):
        put(archive_path, "/tmp/")
        archive_file = archive_path[9:]
        server_archive = "/tmp/{}".format(archive_file)

        archive_base, ext = os.path.splitext(archive_file)
        new_path = "/data/web_static/releases/{}".format(archive_base)

        run("sudo mkdir -p {}".format(new_path))
        run("sudo tar -zxf {} -C {}".format(server_archive, new_path))
        run("sudo rm  {}".format(server_archive))
        run("sudo mv {}/web_static/* {}".format(new_path, new_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_path))

        print("New version deployed!")

        return True

    return False
