[![build status](https://travis-ci.org/wvoliveira/bacon.svg?branch=master)](https://travis-ci.org/wvoliveira/bacon)

Bacon
--------

Backs up the files of the servers listed in the setting file.  

Tested
------

Python3 >

How to
------

Download e configure
```bash
git clone git@github.com:wvoliveira/bacon.git
cd bacon
pip3 install -U .
```

```bash
bacon -h

usage: bacon [-h] --config

Backs up the files of the servers listed in the setting file.
https://github.com/wvoliveira/bacon

optional arguments:
  -h, --help  show this help message and exit
  --config  config file
```

Example config file: `/etc/bacon/bacon.ini`.
