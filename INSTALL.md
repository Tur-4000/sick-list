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