#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric import task, Connection
from datetime import datetime
import os

env = {"hosts": ['54.221.100.63', '34.234.69.221'], "user": "ubuntu", "key": "~/.ssh/id_rsa"}


def do_pack():
    """Function to generate a .tgz archive from the contents of the web_static folder."""
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    os.system("mkdir -p versions")
    archive_path = f"versions/web_static_{time_stamp}.tgz"
    os.system(f"tar -cvzf {archive_path} web_static")
    if os.path.exists(archive_path):
        return archive_path
    else:
        return None


def do_deploy(c, archive_path):
    """Function to distribute an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name
        c.put(archive_path, "/tmp/")
        c.run(f"mkdir -p {path_name}/")
        c.run(f'tar -xzf /tmp/{file_name} -C {path_name}/')
        c.run(f"rm /tmp/{file_name}")
        c.run(f"mv {path_name}/web_static/* {path_name}/")
        c.run(f"rm -rf {path_name}/web_static")
        c.run(f'rm -rf /data/web_static/current')
        c.run(f'ln -s {path_name}/ /data/web_static/current')
        return True
    except Exception as e:
        print(e)
        return False


@task
def deploy(c):
    """Create and distribute an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(c, archive_path)
