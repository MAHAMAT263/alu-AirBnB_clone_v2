#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['3.84.176.255', '54.236.6.241']
env.user = 'ubuntu'
env.key_filename = ['root/.ssh/id_rsa']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(archive_name))

        # Uncompress the archive to the folder
        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_name, folder_name))

        # Remove the archive from the web server
        run("rm /tmp/{}".format(archive_name))

        # Move content to proper location
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(folder_name, folder_name))

        # Remove the symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(folder_name))

        print("New version deployed!")

        return True
    except Exception as e:
        print(e)
        return False

