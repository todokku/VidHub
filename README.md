# VidHub


## Setup a development environment
* Set up a VM with Debian 10 (Web + SSH server; hostname 'vidhub') 

* Install git (`apt install git`)

* Install mysql (`apt install mariadb-server`)
  * Run the included `mysql_secure_installation` security script to restrict access to the server
  * Create the vidhub user (`GRANT ALL ON *.* TO 'vidhub'@'localhost' IDENTIFIED BY 'sommer' WITH GRANT OPTION;`)
  * Create the database (`mysql -u vidhub -p -e 'create database vidhub;'`)

* Install default-libmysqlclient-dev (`apt install default-libmysqlclient-dev`)
* Install redis server (`apt install redis-server`)
* Install ffmpeg (`apt install ffmpeg`)

* Install pip (`apt install python3-venv python3-pip`)
* Install pipenv [pipenv-fork.readthedocs.io](https://pipenv-fork.readthedocs.io/en/latest/install.html#pragmatic-installation-of-pipenv)

* Clone the vidhub repo (or a fork of it)
* Install dependencies using pipenv (`pipenv shell && pipenv install --dev`)
* Run `./manage.py migrate`
