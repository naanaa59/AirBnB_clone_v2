#!/usr/bin/python3
"""Create and distributes an archive to web servers"""
from time import sleep
import os.path
import time
from fabric.api import local
from fabric.operations import env, put, run

env.hosts = ["54.158.203.28", "52.91.156.191"]


def do_pack():
    """Generate an tgz archive from web_static folder"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return ("versions/web_static_{}.tgz".format(time.
                                                    strftime("%Y%m%d%H%M%S")))
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if (os.path.isfile(archive_path) is False):
        return False

    # try:
    file = archive_path.split("/")[-1]
    folder = ("/data/web_static/releases/" + file.split(".")[0])
    put(archive_path, "/tmp/")
    run("mkdir -p {}".format(folder))
    run("tar -xzf /tmp/{} -C {}".format(file, folder))
    run("rm /tmp/{}".format(file))
    run("mv {}/web_static/* {}/".format(folder, folder))
    run("rm -rf {}/web_static".format(folder))
    run('rm -rf /data/web_static/current')
    run("ln -s {} /data/web_static/current".format(folder))
    print("Deployment done")
    return True
    # except Exception as e:
    # return False


def deploy():
    """Create and distributes an archive to web servers"""
    # try:
    path = do_pack()
    return do_deploy(path)
    # except Exception as e:
    # return False


def do_clean(number=0):
    """
        deletes out-of-date archives depending on number value:
            number=0 or number=1 : delete all except most recent version
            number=2: keep 2 most recent versions
            etc
    """
    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1
    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | sudo xargs rm -rf'.format(path, number))
