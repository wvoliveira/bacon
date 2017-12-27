#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Backs up the files of the servers listed in the setting file
"""

import ConfigParser
import subprocess
import logging
import tarfile
import os
import datetime
import time
import sys
import argparse
import json
import requests

parser = argparse.ArgumentParser(description='Backs up the files of the servers listed in the setting file')
parser.add_argument('-c', '--config', metavar='\b', help='config file', required=True)
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def check_dependencies():
    try:
        subprocess.check_output(['which', 'rsync'])
    except subprocess.CalledProcessError:
        logging.warn("Este script precisa do 'rsync'.")
        logging.warn("Debian: sudo apt install 'rsync'")
        logging.warn("CentOS/RedHat: sudo yum install 'rsync'")
        exit(1)


def config_parser(section):
    config = ConfigParser.ConfigParser()
    config.read(args.config)
    if config.has_section(section):
        items_dict = dict(config.items(section))
        return items_dict
    else:
        logging.error("Variavel '{0}' inexistente no arquivo de configuracao".format(section))
        sys.exit(1)


def tarfile_make(source, destination):
    try:
        with tarfile.open(destination, "w:gz") as tar:
            tar.add(source, arcname=os.path.basename(source))
    except Exception as error:
        logging.error(error)
        pass


def sync(options, source, destination):
    try:
        sync_command = 'rsync {0} {1} {2}'.format(options, source, destination)
        sync_result = subprocess.Popen(sync_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (sync_out, sync_err) = sync_result.communicate()
        return sync_err
    except Exception as error:
        logging.error('Sync source: {0}'.format(error))
        pass


def slack_send(url, channel, message):
    try:
        slack_data = {'channel': channel, 'text': message}
        response = requests.post(
            url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            logging.error("Request to slack returned '{0}': {1}".format(response.status_code, response.text))
    except Exception as error:
        logging.error(error)
        pass


def main():

    check_dependencies()

    sync_config = config_parser('rsync')
    backup_config = config_parser('backup')
    hosts_config = config_parser('user_host_path')

    day_name = datetime.datetime.now().strftime('%A').lower()

    logging.debug('Loading user and hosts in settings.ini')
    for user_host in sorted(hosts_config):

        if '@' in user_host:
            hostname = user_host.split('@')[1]
        else:
            hostname = user_host
        logging.info('Hostname: {0}'.format(hostname))

        directories = hosts_config[user_host].split()
        logging.info('Directories: {0}'.format(directories))

        sync_destination = '{0}/{1}/'.format(sync_config['destination'].rstrip('/'), hostname)
        logging.info('Sync destination path: {0}'.format(sync_destination))

        backup_destination = '{0}/{1}/'.format(backup_config['destination'].rstrip('/'), hostname)
        logging.info('Backup destination path {0}'.format(backup_destination))

        try:
            logging.debug('Verifying sync destination path')
            if not os.path.exists(sync_destination):
                os.makedirs(sync_destination)

            if not os.path.exists(backup_destination):
                os.makedirs(backup_destination)

        except OSError as os_error:
            logging.critical('Error to create directories: {0}'.format(os_error))

        logging.debug('Loading directory in directory list')

        for directory in directories:
            source_path = '{0}:{1}'.format(user_host, directory)
            logging.info('Source path: {0}'.format(source_path))
            sync_err = sync(sync_config['options'], source_path, sync_destination)

            if sync_err is not None and len(sync_err) > 5:
                logging.critical(sync_err.rsplit('\n')[0])

        tarfile_path = '{0}{1}-{2}-{3}.tar.gz'.format(backup_destination, hostname, day_name, time.time())
        logging.info('Destination path: {0}'.format(tarfile_path))
        tarfile_make(sync_destination.rstrip('/'), tarfile_path)


if __name__ == '__main__':
    main()
