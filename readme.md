# Документация

## Регистрация
POST /register

__Request body__

phone: string
Должен быть уникальным. Формат: строго 12 символов +7XXXXXXXXXX, только цифры и знак + в начале строки.

password: string
Пароль пользователя. Должен быть надёжным.

password_retype: string
Подтверждение пароля. Должен совпадать с password.

__Response__
200 Успех

phone: string
Номер телефона (идентификатор) созданного пользователя

400 Ошибка в переданных параметрах
ErrorMessage: string
Номер телефона уже существует; неверный формат; пароль ненадежный; пароли не совпадают

500 Ошибка сервера
_____
## Аутентификация
POST /login

__Request body__

Phone: string
Password: string 

__Response__
200 Успех

Access: string
Refresh: string

400 Ошибка в переданных данных
500 Ошибка сервера
_____
## Обновление access токена
POST /token/refresh

__Request body__
Refresh: string

__Response__
200 Успех
Access: string
Refresh: string

401 Не авторизован
refresh токен истек

500 Ошибка севера

____
## Подтверждение регистрации
(На уточнении)
GET /register/confirm?phone={}&confirmation={}
Код подтверждения приходит в смс по номеру телефона

__Response__
200 Успех
404 Параметры запроса неверные
500 Ошибка севера
____
## Восстановление пароля
(возможно будет реализовано позднее)
___
## Получение списка паркингов (для владельца)
GET /api/parks/

__появилась информация о ценах__
___
## Получение конкретного паркинга (для владельца)
GET /api/parks/{id}/ 

__появилась информация о ценах__
___
## Получение списка парковок (для пользователя)
GET /api/parkings/ (записи о парковках сортируются по entry_time от самой новой до самой старой)

__появился расчет цены, время теперь локальное (по местоположению паркинга) и UTC__

![изображение](https://user-images.githubusercontent.com/82332119/210776663-26d520ba-6cd5-4e0b-9ce8-72bd7d35cf84.png)

___
## Добавление новой записи о заезде на паркинг
POST api/entry-register/

:bangbang: теперь, если машина не зарегистрирована в сервисе её номер отображается как unregistred

![изображение](https://user-images.githubusercontent.com/82332119/237043864-82499c7a-535d-42ce-9c72-baf39a60bae8.png)


__Request body__
park: int
car: string (номер машины)

__Response__
201 Created
400 Ошибка в переданных данных
___
## Добавление новой записи о выезде с паркинга
POST api/checkout-register/

:bangbang: теперь, если машина не зарегистрирована в сервисе её номер отображается как unregistred и дополнительно приходит confirmation_code

![изображение](https://user-images.githubusercontent.com/82332119/237044139-52bc98e7-198b-4356-814b-a003f7b5b141.png)

__Request body__
park: int
car: string 

__Response__
201 Created
400 Ошибка в переданных данных
___
## Создание новой парковки
(сейчас может выполнить любой пользователь прошедший аутентификацию)
(хозяином парковки устанавливается пользователь выполнивший запрос)
POST /api/parks/create

__Request body__
description: string 
place_count: int
latitude: decimal (с точностью 6 знаков после запятой)
longitude: decimal (с точностью 6 знаков после запятой)

опционально 
address: string
web_address: string

__Response__
201 Created
400 Ошибка в переданных данных
___
## CRUD для машины
GET /api/cars - отдает список машин пользователя

POST :bangbang: ~~/api/cars~~ /api/add-car/ - создает новую машину для пользователя 
теперь обязательным является код подтверждения

![изображение](https://user-images.githubusercontent.com/82332119/237043046-c4293b37-379d-40fa-a0df-4186db093769.png)

PUT, PATCH, DELETE /api/cars/<номер машины (он же PK)> - редактирует, удалеят машину пользователя с переданным PK
____
## Задать цену для паркинга

список возможных значений для day_of_week:
- ALL = "All"
- WEEKEND = "Wkd"
- MONDAY = "Mon"
- THUESDAY = "Tue"
- WEDNESDAY = "Wed"
- THURSDAY = "Thu"
- FRIDAY = "Fri"
- SATURDAY = "Sat"
- SUNDAY = "Sun"

сначала выбирается цена по дню недели -> если такой нет -> WEEKEND (если выходной день) -> ALL (если нет не выбрано на предыдущих шагах)

POST /api/price - создает новую цену

PUT, PATCH, DELETE /api/price/<PK> - редактируем, удаляем цену
____
## Профиль пользователя

get profile/ - отдает профиль пользователя

PATCH profile/ - редактирует профиль
____
## Пагинация
На ендпоинтах отдающих коллекции подключена пагинация в стиле limit-offset

Пример:

Запрос /api/parkings/?limit=2&offset=3 отдаст 2 записи о парковках пользователя со смещением в 3 элемента от начала коллекции (т. е. запрос отдаст 4, 5 записи). Для получения последней записи достаточно установить параметру limit значение 1 (параметр offset можно опустить)

При использовании пагинации ответ выглядит следующим образом:
![изображение](https://user-images.githubusercontent.com/82332119/206853922-30647849-3243-442e-906b-73ca18450fd0.png)
