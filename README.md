[![build status](https://travis-ci.org/wvoliveira/backupon.svg?branch=master)](https://travis-ci.org/wvoliveira/backupon)

Backupon
--------

Faz o backup de arquivos e diretórios de servidores se baseando no arquivo de configuração.  

Características:
- [x] Arquivo de configuracao - Nao precisa alterar nenhuma caracteristica dentro do script

Para realizar um teste local:  

Caso seu sistema operacional seja baseado em Debian, use o apt-get, caso seja baseado em CentOS/RedHat, use yum. Vamos supor que iremos rodar o script num Debian:  

Instale o rsync: `apt-get install -y rsync`  
Instale o ssh (client e server): `apt-get install -y ssh`  
Inicie o serviço do ssh server: `service ssh start`  
Gere uma chave para usar na autenticação por ssh com o seu usuário: `echo -e "\n\n\n" | ssh-keygen`  
Copie o arquivo de exemplo: `cp settings.ini.example settings.ini`  
Crie o diretorio que armazenará os arquivos sincronizados: `mkdir /tmp/backup`  
Crie o diretório que servirá de armazenamento dos arquivos compactados: `mkdir /tmp/path_mounted`  
Crie os diretórios que iremos realizar o backup: `/tmp/teste{01..05}`  
Crie alguns arquivos dentro desses diretórios: `touch /tmp/teste{01..05}/file{01..05}`  
Adicione os hostnames contidos no arquivo de configuração para serem resolvidos como localhost:  
```
echo '127.0.0.1		vm-server01.servers' >> /etc/hosts
echo '127.0.0.1		vm-server02.servers' >> /etc/hosts
echo '127.0.0.1		vm-server03.servers' >> /etc/hosts
echo '127.0.0.1		vm-server04.servers' >> /etc/hosts
echo '127.0.0.1		vm-server05.servers' >> /etc/hosts
```
Execute o script: python backupon.py -c settings.ini  
Leia o arquivo de log: `tailf /tmp/backupon.log`  

O output será desse jeito:  
```
2017-06-19 11:48:12,936 INFO     Hostname: vm-server01.servers
2017-06-19 11:48:12,937 INFO     Directories: ['/tmp/teste01', '/tmp/teste01', '/tmp/teste01', '/tmp/teste01']
2017-06-19 11:48:12,937 INFO     Sync destination path: /tmp/backup/vm-server01.servers/
2017-06-19 11:48:12,937 INFO     Backup destination path /tmp/path_mounted/vm-server01.servers/
2017-06-19 11:48:14,679 INFO     Destination path: /tmp/path_mounted/vm-server01.servers/vm-server01.servers-monday-1497883694.68.tar.gz
```
