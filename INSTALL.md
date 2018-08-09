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
$ adduser --gecos "" <sicklist username>
# целесообразность включения в группу sudo под вопросом
$ usermod -aG sudo <sicklist username>
$ su <sicklist username>
```

## Установка приложения

### Клонирование репозитория

В домашнем каталоге пользователя <sicklist username> выплнить команды

``` bash
$ git clone https://github.com/Tur-4000/sick-list.git
$ cd sick-list
# на всякий случай
$ git checkout master
``` 

## Подготовка виртуальной среды

``` bash
$ cd /home/<sicklist username>/sik-list
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ pip install gunicorn pymysql
```

Создать файл .env с необходимыми переменными среды

``` bash
$ vim /home/<sicklist username>/sik-list/.env
```

Содержимое файла .env

```
SECRET_KEY=52cb883e323b48d78a0a36e8e951ba4a
MAIL_SERVER=localhost
MAIL_PORT=25
DATABASE_URL=mysql+pymysql://<sicklist db username>:<db-password>@localhost:3306/sicklist
```

SECRET_KEY можно сгенерировать командой
``` bash
python3 -c "import uuid; print(uuid.uuid4().hex)"
```

Задать переменную среды FLASK_APP
От имени пользователя <sicklist username> выполнить команду
``` bash
$ echo "export FLASK_APP=microblog.py" >> ~/.profile
```

### Настройка MySQL

Подключиться к MySQL
пароль задавался при инсталляции MySQL (в ubuntu 18.04 использовать sudo mysql без указания пользователя)

``` bash
$ mysql -u root -p
```

Создать базу данных и пользователя с полным доступом к этой базе данных

``` bash
mysql> create database sicklist character set utf8 collate utf8_bin;
mysql> create user '<sicklist db username>'@'localhost' identified by '<db-password>';
mysql> grant all privileges on sicklist.* to '<sicklist db username>'@'localhost';
mysql> flush privileges;
mysql> quit;
```

Запустить процесс миграции базы данных

``` bash
(venv) $ flask db upgrade
```

### Настройка Gunicorn и Supervisor

Выполняются пользователем с правами root

Создать конфигурацию supervisor для sicklist

``` bash 
$ sudo vim /etc/supervisor/conf.d/sicklist.conf
```
Содержимое файла sicklist.conf

```
[program:sicklist]
command=/home/<sicklist username>/sik-list/venv/bin/gunicorn -b localhost:8000 -w 2 sicklist:app
directory=/home/<sicklist username>/sik-list
user=<sicklist username>
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

Перезапустить supervisor

``` bash
$ sudo supervisorctl reload
```

### Настройка Nginx

* Выполняется пользователем <sicklist username>
#### Создание самоподписанных сертификатов
``` bash
$ cd /home/<sicklist username>/sik-list
$ mkdir certs
$ openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout certs/key.pem -out certs/cert.pem
```
В результате в каталоге /home/<sicklist username>/sik-list/certs должны появится файлы key.pem и cert.pem

* Выполняется пользователем с правами root
#### Файл конфигурации NGINX

``` bash
$ sudo rm /etc/nginx/sites-enabled/default
```

``` bash
$ sudo vim /etc/nginx/sites-enabled/sicklist
```

Содержимое файла /etc/nginx/sites-enabled/sicklist

```
server {
    # прослушивание порта 80 (http)
    listen 80;
    server_name _;
    location / {
        # перенаправлять любые запросы на один и тот же URL-адрес, как на https
        return 301 https://$host$request_uri;
    }
}
server {
    # прослушивание порта 443 (https)
    listen 443 ssl;
    server_name _;

    # расположение self-signed SSL-сертификата
    ssl_certificate /home/<sicklist username>/sik-list/certs/cert.pem;
    ssl_certificate_key /home/<sicklist username>/sik-list/certs/key.pem;

    # запись доступа и журналы ошибок в /var/log
    access_log /var/log/sicklist_access.log;
    error_log /var/log/sicklist_error.log;

    location / {
        # переадресация запросов приложений на сервер gunicorn
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # обрабатывать статические файлы напрямую, без пересылки в приложение
        alias /home/<sicklist username>/sik-list/static;
        expires 30d;
    }
}
```

Перезапуск NGINX

``` bash
$ sudo service nginx reload
```
