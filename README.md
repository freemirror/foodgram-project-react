
## _Foodgram «Продуктовый помощник»_
Проект представляет из себя онлайн-сервис Foodgram «Продуктовый помощник» и REST API модуль к нему.
Проект позволяет через различные приложения, http запросы, публиковать свои рецепты, просматривать рецепты других пользователей, добавлять рецепты в избранное, подписываться на публикации других пользователей добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

- Не авторизованные пользователи могут просматривать рецепты на главной странице и на страницах пользователей, просматривать детальную информацию по рецепту и фильтровать рецепты по тегам.
- Авторизованные пользователи помимо этого могут создавать/редактировать/удалять собственные рецепты, работать с персональными списками избранного и списка покупок, подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок, а так же выгружать сводный список ингредиентов по списку покупок.
- Администратор обладает всеми правами авторизованного пользователя и может так же изменять пароль любого пользователя, создавать/блокировать/удалять аккаунты пользователей, редактировать/удалять любые рецепты, добавлять/удалять/редактировать любые теги и ингредиенты. Все эти функции реализованы в административной панели.

Получение доступа по токену реализовано чрезе модуль библиотеки rest_framework, TokenAuthentication.

### Запуск приложения в контейнерах(локально):

1) Клонировать репозиторий и перейти в корневую папку.
Находясь в корневой папке проекта ввести в терминале(Bash) команду
```
git clone git@github.com:freemirror/foodgram-project-react.git
```
2) Вводим пароль и переходим в папку infra, введя команду.
```
cd infra/
```
3) Создаем в ней файл .env с переменными окружения необходимыми для работы приложения
Пример заполнения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

4) Далее запускаем docker-compose командой:
```
docker-compose up -d
```

5) Далее внутри контейнера web выполняем миграции, создаем суперпользователя, собираем статику и загружаем список ингредиентов:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
docker-compose exec web python manage.py load_csv
```

Проект доступен по адресу: 
http://84.252.143.131/

Логин/пароль администратора (для проверки):
freem@ya.ru/AjlAx1990 (для админики freem, пароль тот же)

Остановка контейнеров:

docker-compose stop

Запуск контейнеров:

docker-compose start


Для приложения настроено Continuous Integration и Continuous Deployment.
При пуше изменений в ветку master в репозиторий на github проиходит:
- Проверка кода на соответствие стандартам PEP8
- Сборка и доставка докер-образа для контейнера web на Docker Hub
- Автоматический деплой проекта на боевой сервер

### Примеры запросов к API:
```
POST http://84.252.143.131/api/users/
Authorization: token b8d4f4872a9ab02d1cb52f68d25e2f660840bd11
Content-Type: application/json
{
"email": "valentina@yandex.ru",
"username": "valya1995",
"first_name": "Валентина",
"last_name": "Иванова",
"password": "Qwerty123"
}
```
```
GET http://84.252.143.131/api/recipes/download_shopping_cart/
```
```
DELETE http://84.252.143.131/api/recipes/3/favorite/
```
```
GET http://84.252.143.131/api/ingredients/123/
```
