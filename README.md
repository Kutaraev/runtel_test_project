# Тестовое задание

## Установка проекта
1. Скопировать проект в любую директорию.
2. Сделать данную директорию текущей.
3. Выполнить команду `docker compose up`.

После выполнения этих действий поднимутся два контейнера: один с БД PostgreSQL, другой с aiohttp-сервером. Далее с помощью alembic производится миграция, создающая схему в БД, и запускается скрипт `data_loader.py`, который копирует тестовые данные из `data_to_import.json` в БД. Приложение готово к работе.

## Описание моделей

#### User
Регистрационные данные пользователя. Имеет следующие поля:
 - `username` - логин пользователя, тип `str`.
 - `password` - пароль пользователя, тип `str` (в БД хранится в хешированном виде).

 Модель `User` связана один-к-одному с моделью `Profile`, и один-ко-многим с моделью `Animals`.

#### Profile
Профиль пользователя. Имеет слевующие поля:
- `firstname` - имя пользователя, тип `str`.
- `lastname` - фамилия пользователя, тип `str`.
- `user_id` - `id` пользователя, тип `int`.

#### Animal
Домашнее животное пользователя. Имеет следующие поля:
- `type` - вид животного, тип `str`.
- `name` - имя животного, тип `str`.
- `age` - возраст животного, тип `int`.
- `user_id` - `id` пользователя, тип `int`.

## REST-запросы

#### Ресурс users
**Список всех пользователей**  
Пример запроса:
```
curl --location 'http://0.0.0.0:8080/users'
```
Пример ответа:
```
[{"id": 1, "username": "test_user_1"}, {"id": 2, "username": "test_user_2"}, {"id": 3, "username": "test_user_3"}, {"id": 4, "username": "test_user_4"}, {"id": 5, "username": "test_user_5"}, {"id": 6, "username": "test_user_6"}, {"id": 7, "username": "test_user_7"}, {"id": 8, "username": "test_user_8"}, {"id": 9, "username": "test_user_9"}, {"id": 10, "username": "test_user_10"}, {"id": 11, "username": "test_user_11"}, {"id": 12, "username": "test_user_12"}]
```
**Создать нового пользователя**  
Пример запроса:
```
curl --location 'http://0.0.0.0:8080/users' \
--header 'Content-Type: application/json' \
--data '{"username": "JohnDoe", "password": "qwerty"}'
```
Пример ответа:
```
{"message": "user JohnDoe successfully created!"}
```
**Изменить данные пользователя**  
Пример запроса:
```
curl --location --request PUT 'http://0.0.0.0:8080/users/1' \
--header 'Content-Type: application/json' \
--data '{"username": "changed username", "password": "changed password"}'
```
Пример ответа:
```
{"id": 1, "username": "changed username"}
```
**Удалить пользователя**  
Пример запроса:
```
curl --location --request DELETE 'http://0.0.0.0:8080/users/8'
```
Пример ответа:
```
   
```
### Ресурс profile  
**Получить профиль пользователя**  
Пример запроса:
```
curl --location 'http://0.0.0.0:8080/users/5/profile'
```
Пример ответа:
```
{"profile_id": 2, "firstname": "name_5", "lastname": "lastame_5", "user_id": 5}
```
**Создать профиль пользователя**  
Пример запроса:
```
curl --location 'http://0.0.0.0:8080/users/6/profile' \
--header 'Content-Type: application/json' \
--data '{"firstname": "John", "lastname": "Doe"}'
```
Пример ответа:
```
{"message": "profile John successfully created!"}
```
**Изменить профиль пользователя**  
Пример запроса:
```
curl --location --request PUT 'http://0.0.0.0:8080/users/6/profile' \
--header 'Content-Type: application/json' \
--data '{"firstname": "Jane", "lastname": "Doe"}'
```
Пример ответа:
```
{"id": 4, "firstname": "Jane", "lastname": "Doe"}
```
**Удалить профиль пользователя**  
Пример запроса:
```
curl --location --request DELETE 'http://0.0.0.0:8080/users/6/profile'
```
Пример ответа:
```
 
```

### Ресурс animals  

**Получить список животных пользователя**  
Пример запроса:
```
curl --location 'http://0.0.0.0:8080/users/1/animals'
```
Пример ответа:
```
[{"id": 1, "type": "cat", "name": "cat_name", "age": 1}, {"id": 2, "type": "dog", "name": "dog_name", "age": 3}]
```
**Создать животное**  
Пример запроса:
```
curl --location 'http://0.0.0.0:8080/users/2/animals' \
--header 'Content-Type: application/json' \
--data '{"type": "turtle", "name": "Leonardo", "age": 15}'
```
Пример ответа:
```
{"message": "animal Leonardo successfully created!"}
```
**Изменить данные о животном**  
Пример запроса:
```
curl --location --request PUT 'http://0.0.0.0:8080/users/2/animals/4' \
--header 'Content-Type: application/json' \
--data '{"type": "turtle", "name": "Raphael", "age": 16}'
```
Пример ответа:
```
{"type": "turtle", "name": "Raphael", "age": 16}
```
**Удалить животное**  
Пример запроса:
```
curl --location --request DELETE 'http://0.0.0.0:8080/users/2/animals/4'
```
Пример ответа:
```
 
```