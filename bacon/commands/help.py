import subprocess
import configparser
import tarfile
import os


def depends():
    needed = ['rsync']
    to_install = list()

    for app in needed:
        try:
            subprocess.check_output(['which', app])
        except subprocess.CalledProcessError:
            to_install.append(app)

        return to_install


def parser_me(file):
    config = configparser.ConfigParser()
    config.read(file)
    items = dict()
    for section in config.sections():
        items[section] = dict(config.items(section))
    return items


def compress(src, dest):
    with tarfile.open(dest, "w:gz") as tar:
        tar.add(src, arcname=os.path.basename(src))


def sync(options, src, dest):
    command = 'rsync {0} {1} {2}'.format(options, src, dest)
    result = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    return err
