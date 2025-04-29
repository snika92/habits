## Установка проекта локально:

Приложение написано на языке Python, для его установки 

Клонируйте репозиторий:

Для SSH:
```
git@github.com:YanaSozoniva/healthy-habits-tracker.git
```

## Запуску проекта через docker-compose и проверка работоспособности

1. Установите Docker (для этого скачайте Docker Desktop с офицального сайта для вашей операционной системы: https://www.docker.com/products/docker-desktop.) 
2. Для запуска приложения введите команду в терминале: 
docker-compose up -d --build
3. После успешного запуска Django-приложение будет доступно по адресу http://localhost:8000

4. Для проверки запущенных контейнеров и их состояния введите команду:
 docker-compose ps

5. Для просмотра логов всех контейнеров (для отладки и мониторинга работы контейнеров) введите команду:
 docker-compose logs

##  Инструкция по настройке сервера и CI/CD

1. Для подключения к серверу введите команду в терминале: ssh -l ubuntu 158.160.0.255
2. Для обновления системы и установки всех пакетов введите команды: sudo apt update, sudo apt upgrade
3. Установите Docker (см. пункт выше)
4. Настройте файрвол: 
   1. sudo ufw status
   2. sudo ufw enable
   3. sudo ufw allow 80/tcp
   4. sudo ufw allow 443/tcp
   5. sudo ufw allow 22/tcp
   6. sudo ufw status
5. Установите Git: sudo apt update
                   sudo apt install git
6. Клонируйте репозиторий: git clone git@github.com:YanaSozoniva/healthy-habits-tracker.git
7. Перейдите в созданный репозиторий: cd healthy-habits-tracker
8. Заполните файл с переменными окружения: nano .env
9. Выполните команду для запуска контейнеров: docker-compose up -d
    Адрес сервера с развернутым приложением http://158.160.0.255:8000/
