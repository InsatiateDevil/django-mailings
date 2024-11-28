# Сервис управления рассылками

## Описание проекта

Это проект Django, предназначенный для рассылки писем клиентам пользователей 
по определенному расписанию. Он позволяет пользователям регистрироваться, 
просматривать и редактировать свои рассылки, клиентов и сообщения, а также просматривать 
статьи в блоге.

## Установка

Скачайте и распакуйте архив проекта.
Откройте терминал и перейдите в папку проекта.
Настройте виртуальное окружение проекта, подготовьте БД, а также при кэшировании - брокер(redis).
Произведите заполнение .env файла на примере .env.sample.
Введите команды для запуска сервера Django, а так же Celery и Flower:

    запуск сервера Django - python3 manage.py runserver

    запуск Flower отдельно от Celery - celery -A config flower

    запуск Celery worker - celery -A config worker -l INFO
    
    запуск Celery beat - celery -A config beat -S django -l info

## Заполнение данными

Для заполнения базы данных данными, используйте команду 

    python manage.py migrate
и затем 

    python manage.py loaddata db.json 
Эти команды настроят БД под нужды проекта, а так же произведут наполнение 
некоторыми стандартными данными из фикстуры

## Настройка проекта
Проект использует стандартные настройки Django и не требует дополнительной
настройки. Однако, вы можете изменить настройки проекта в файле settings.py.
Обязательно не забудьте создать и заполнить файл .env(по примеру .env.sample).
Разработка проекта ведется на связке pip-venv и список необходимых для работы
проекта библиотек хранится в requirements.txt в корневом каталоге проекта.
