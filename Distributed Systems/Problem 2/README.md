# Problem 2. Two-Phase Commit Protocol

Formaulation of the problem: [Lab_2-2PC.docx]()

Pre-requirements:
- Python 3.x
- pip
- pgAdmin4 (optional)
- pyvenv

Install PostgreSQL [[source](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)]:
```sh
$ sudo apt-get install postgresql postgresql-contrib
```
Install python requirements:
```sh
$ pip install -r requirements.txt
```
Run script:
```sh
$ python dtc.py
```
#### [Optional] Install pgAdmin4 [[source](https://askubuntu.com/questions/831262/how-to-install-pgadmin-4-in-desktop-mode-on-ubuntu)]:
Set up environment
```sh
$ python3 -m venv /path/to/venv/
$ source /path/to/venv/bin/activate
$ pip install https://ftp.postgresql.org/pub/pgadmin/pgadmin4/v2.1/pip/pgadmin4-2.1-py2.py3-none-any.whl
```
Create and configure local file
```sh
gedit /path/to/venv/lib/python3.x/site-packages/pgadmin4/config_local.py
```
Write:
```
import os
DATA_DIR = os.path.realpath(os.path.expanduser(u'/path/to/venv/venv-name/'))
LOG_FILE = os.path.join(DATA_DIR, 'pgadmin4.log')
SQLITE_PATH = os.path.join(DATA_DIR, 'pgadmin4.db')
SESSION_DB_PATH = os.path.join(DATA_DIR, 'sessions')
STORAGE_DIR = os.path.join(DATA_DIR, 'storage')
SERVER_MODE = False
```
Run:
```sh
python /path/to/venv/lib/python3.x/site-packages/pgadmin4/pgAdmin4.py
```
(Also `start_pgadmin.sh` can be updated with your venv path and can be started with bash)
Access `127.0.0.1:5050` and set path to binary as `/usr/bin/`.
