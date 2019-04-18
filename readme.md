```
Зависимости:

sudo apt install libaprutil1-dev

Создаём virtualenv:

HOME_DIR="/home/elastic/_project/es"  (для примера)

$ cd ${HOME_DIR}
$ virtualenv -p `which python3` .venv3

Акивируем вирт.среду:
$ . ${HOME_DIR}/.venv3/bin/activate

Устанавливаем необходимые пакеты:
(.venv3) $ pip install -r requirements.txt

Инициализируем БД для авторизации пользователей (sqlite3):
(.venv3) $ python manage.py db init
(.venv3) $ python manage.py db migrate
(.venv3) $ python manage.py db upgrade

В ./secret/.htpasswd создаем учетную запись (суперпользователя):
$ htpasswd -c /secret/.htpasswd root

Параметры подключения БД mysql, ElasticSearch и т.п.) здесь:
./instance/config.py

Запуск в debug-mode:
./run_debug.sh


```