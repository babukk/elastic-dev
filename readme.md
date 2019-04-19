```
Зависимости:

sudo apt install libaprutil1-dev

Создаём virtualenv:

HOME_DIR="/home/elastic/_project/es"  (для примера)

$ cd ${HOME_DIR}
$ virtualenv -p `which python3` .venv3

Активируем вирт.среду:
$ . ${HOME_DIR}/.venv3/bin/activate

Устанавливаем необходимые пакеты:
(.venv3) $ pip install -r requirements.txt

Инициализируем БД для авторизации пользователей (sqlite3 в данном случае):
(.venv3) $ python manage.py db init
(.venv3) $ python manage.py db migrate
(.venv3) $ python manage.py db upgrade

В ./secret/.htpasswd создаем учетную запись (суперпользователя):
$ htpasswd -c /secret/.htpasswd root

Параметры подключения БД mysql, ElasticSearch и т.п.) здесь:
./instance/config.py

Запуск в debug-mode:
./run_debug.sh


Для запуска в production рекомендуется связка nginx + uwsgi-emperor:
sudo apt install nginx uwsgi-emperor uwsgi-plugin-pythoh

Пример (в стиле Debian/Ubintu) ini-файла для uwsgi-emperor:
./deploy/etc/uwsgi-emperor/vassals/es.ini

Пример (в стиле Debian/Ubintu) conf-файла для nginx:
./deploy/etc/nginx/sites-available/es.conf
и symbolic-линк:
./deploy/etc/nginx/sites-enable/es.conf -> ../sites-available/es.conf

systemctl restart uwsgi-emperor
systemctl restart nginx


```