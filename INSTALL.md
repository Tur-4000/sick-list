# Сценарий инсталляции на виртуальную машину с ubuntu 16.04

## Базовые зависимости

### Установка необходимых пакетов

* python3 
* python3-venv 
* python3-dev
* mysql-server 
* postfix 
* supervisor 
* nginx 
* git

``` bash
$ sudo apt-get -y update
$ sudo apt-get -y install python3 python3-venv python3-dev
$ sudo apt-get -y install mysql-server postfix supervisor nginx git
```

### Настройка файрвола

Открыть 80 и 443 порты на файрволе (если будет использоваться нестандартный порт, открыть и его):

``` bash
$ sudo ufw allow http
$ sudo ufw allow 443/tcp
```

### Создание пользователя

Создать пользователя от имени которого будет работать система

``` bash
$ adduser --gecos "" <siklist username>
# целесообразность включения в группу sudo под вопросом
$ usermod -aG sudo <siklist username>
$ su <siklist username>
```
