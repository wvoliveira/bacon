"""
Backs up the files of the servers listed in the setting file
"""

import logging
import datetime
import time
import sys
import argparse
from colorama import Fore
from .commands import *

CRITIC = '{}[!]{}'.format(Fore.RED, Fore.RESET)

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""Backs up the files of the servers listed in the setting file. \nhttps://github.com/wvoliveira/bacon""")
parser.add_argument('--config', default='/etc/bacon/bacon.ini', metavar='\b', help='config file', required=True)
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')


def main():
    apps = depends()
    if len(apps) > 0:
        logging.error("{} I could't find these apps: {}".format(CRITIC, ' '.join(apps)))
        exit(1)

    day = datetime.datetime.now().strftime('%A').lower()

    logging.info('[*] Loading rsync, backup and hosts parameters')
    try:
        all_info = parser_me(args.config)
        rsync = all_info['rsync']
        backup = all_info['backup']
        hosts = all_info['hosts']
    except Exception as error:
        logging.error('{} Error to get values: {}'.format(CRITIC, error))
        sys.exit(1)

    logging.info('[*] Loading hosts and paths')
    for host in sorted(hosts):

        hostname = host
        logging.info('[+] Hostname: {0}'.format(hostname))

        directories = hosts[host].split()
        logging.info('[+] Directories: {0}'.format(directories))

        sync_dst = os.path.join(rsync['destination'], hostname)
        logging.info('[+] Sync destination path: {0}'.format(sync_dst))

        bkp_dst = os.path.join(backup['destination'], hostname)
        logging.info('[+] Backup destination path {0}'.format(bkp_dst))

        try:
            logging.info('[*] Creating sync destination path if not exists')
            if not os.path.exists(sync_dst):
                os.makedirs(sync_dst)

            logging.info('[*] Creating backup destination path if not exists')
            if not os.path.exists(bkp_dst):
                os.makedirs(bkp_dst)

        except OSError as os_error:
            logging.critical('{} Error to create directories: {}'.format(CRITIC, os_error))

        logging.debug('[*] Loading directory in directory list')
        for directory in directories:
            source = '{0}:{1}'.format(host, directory)
            logging.info('[+] Source path: {0}'.format(source))

            logging.info('[*] Sync files..')
            sync_err = sync(rsync['options'], source, sync_dst)

            if sync_err is not None and len(sync_err) > 5:
                logging.critical('{} ERRORS: '.format(CRITIC))
                logging.critical(sync_err.rsplit('\n')[0])

        tarfile_path = '{0}{1}-{2}-{3}.tar.gz'.format(bkp_dst, hostname, day, time.time())
        logging.info('[+] Destination path: {0}'.format(tarfile_path))

        logging.info('[*] Compressing files... ')
        compress(sync_dst.rstrip('/'), tarfile_path)


if __name__ == '__main__':
    main()
