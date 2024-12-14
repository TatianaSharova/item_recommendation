# **_Item Recommendation_**
Сервис, ĸоторый анализирует историю поĸупоĸ всех ĸлиентов и
определяет, на ĸаĸие товары предложить сĸидĸи ĸонĸретному пользователю.                                                             

Стек: python, FastAPI, Postgres, SQLAlchemy, pandas, Docker-compose, asyncio, SQLite, pytest.                                                                          
                                           
**Как запустить проект:**
-----------
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/TatianaSharova/item_recommendation.git
```
**_Запуск через Docker-compose:_**                                                 

Создайте файл env. и наполните своими данными:
```
PORT=8000
DB_USER= никнем юзера
DB_PASSWORD= пароль для бд
POSTGRES_PORT=5432
DB_NAME= название бд
```
Запустите проект:          
```
docker compose up --build
```
                                                   
**Примеры запросов:**
-----------
1. Добавление пользователя:
```
POST http://127.0.0.1:8000/users/
Content-Type: application/json
{
  "username": "Kate"
}

```
Ответ:
```
{
  "status": "Пользователь создан.",
  "user_id": "c8a37f4d-5c5a-417d-a870-f7f25e66136d"
}
```
2. Просмотр всех пользователей:
```
Get http://127.0.0.1:8000/users/
```
Ответ:
```
{
  "data": [
    {
      "id": "c8a37f4d-5c5a-417d-a870-f7f25e66136d",
      "username": "Kate"
    },
    {
      "id": "71f51ea5-477b-4011-baab-9e4feed6c8da",
      "username": "Masha"
    },
    {
      "id": "be3c7469-8009-4b2b-9ce6-6daac0db581a",
      "username": "Pasha"
    }
  ]
}
```
3. Создание нового товара:
```
POST http://127.0.0.1:8000/items/
Content-Type: application/json
{
  "name": "white ball",
  "category": "balls"
}

```
Ответ:
```
{
  "status": "Товар создан.",
  "item_id": "5d337106-1132-48cf-97b9-c46145a2800b",
  "data": {
    "name": "white ball",
    "category": "balls"
  }
}
```
4. Просмотр всех товаров:
```
Get http://127.0.0.1:8000/items/
```
Ответ:
```
{
  "data": [
    {
      "id": "5d337106-1132-48cf-97b9-c46145a2800b",
      "name": "white ball",
      "category": "balls"
    },
    {
      "id": "63ab01e4-d21d-41ee-86a8-098c476cabeb",
      "name": "black ball",
      "category": "balls"
    },
    {
      "id": "820074f8-f804-4afc-90a4-b9748532364f",
      "name": "chips",
      "category": "snacks"
    }
  ]
}
```
5. Просмотр товара:
```
Get http://127.0.0.1:8000/items/820074f8-f804-4afc-90a4-b9748532364f/
```
Ответ:
```
{
  "data": {
    "id": "820074f8-f804-4afc-90a4-b9748532364f",
    "name": "chips",
    "category": "snacks"
  }
}
```
6. Создание новой покупки:
```
POST http://127.0.0.1:8000/purchases/
Content-Type: application/json
{
  "user_id": "c8a37f4d-5c5a-417d-a870-f7f25e66136d",
  "cart": [
    {
      "id": "820074f8-f804-4afc-90a4-b9748532364f",
      "category": "snacks"
    },
    {
      "id": "5d337106-1132-48cf-97b9-c46145a2800b",
      "category": "balls"
    }
  ]
}
```
Ответ:
```
{
  "status": "Покупка для пользователя c8a37f4d-5c5a-417d-a870-f7f25e66136d успешно добавлена."
}
```
6. Просмотр всех покупок:
```
Get http://127.0.0.1:8000/purchases/
```
Ответ:
```
{
  "data": [
    {
      "id": "17e01b10-6c0b-4287-9ae4-6ded55c3fb6a",
      "user_id": "c8a37f4d-5c5a-417d-a870-f7f25e66136d",
      "item_id": "820074f8-f804-4afc-90a4-b9748532364f",
      "category": "snacks",
      "purchase_date": "2024-12-14T02:51:54.300874"
    },
    {
      "id": "f7c71055-9fd2-4ec1-958f-260ff5ce82dd",
      "user_id": "c8a37f4d-5c5a-417d-a870-f7f25e66136d",
      "item_id": "5d337106-1132-48cf-97b9-c46145a2800b",
      "category": "balls",
      "purchase_date": "2024-12-14T02:51:54.300874"
    },
    {
      "id": "2c6bc9ad-d3e8-4f5d-910a-420fc609e028",
      "user_id": "be3c7469-8009-4b2b-9ce6-6daac0db581a",
      "item_id": "820074f8-f804-4afc-90a4-b9748532364f",
      "category": "snacks",
      "purchase_date": "2024-12-14T02:55:31.906799"
    },
    {
      "id": "424fecd4-d2e2-4299-9e1d-6b434de56bad",
      "user_id": "be3c7469-8009-4b2b-9ce6-6daac0db581a",
      "item_id": "63ab01e4-d21d-41ee-86a8-098c476cabeb",
      "category": "balls",
      "purchase_date": "2024-12-14T02:55:31.906799"
    }
  ]
}
```
8. Просмотр покупок пользователя по user_id:
```
Get http://127.0.0.1:8000/items/c8a37f4d-5c5a-417d-a870-f7f25e66136d/
```
Ответ:
```
{
  "data": [
    {
      "id": "17e01b10-6c0b-4287-9ae4-6ded55c3fb6a",
      "user_id": "c8a37f4d-5c5a-417d-a870-f7f25e66136d",
      "item_id": "820074f8-f804-4afc-90a4-b9748532364f",
      "category": "snacks",
      "purchase_date": "2024-12-14T02:51:54.300874"
    },
    {
      "id": "f7c71055-9fd2-4ec1-958f-260ff5ce82dd",
      "user_id": "c8a37f4d-5c5a-417d-a870-f7f25e66136d",
      "item_id": "5d337106-1132-48cf-97b9-c46145a2800b",
      "category": "balls",
      "purchase_date": "2024-12-14T02:51:54.300874"
    }
  ]
}
```
9. Сгенерировать рекомендацию для пользователя:
```
POST http://127.0.0.1:8000/generate_recommendations/
Content-Type: application/json
{
  "user_id": "be3c7469-8009-4b2b-9ce6-6daac0db581a"
}
```
Ответ:
```
{
  "status": "Рекомендация успешно сгенерирована."
}
```
10. Просмотр рекомендации для пользователя по id:
```
GET http://127.0.0.1:8000/recommendations?user_id=be3c7469-8009-4b2b-9ce6-6daac0db581a
```
Ответ:
```
{
  "data": {
    "item_id": "5d337106-1132-48cf-97b9-c46145a2800b"
  }
}
```
                                                     
**Тестирование:**                                                 
-----------
Для тестов создается отдельная асинхронная база данных Sqlite.
Для тестирования введите в командной строке:
```
pytest
```
                                                      
**Документация:**                                                               
-----------
Документацию к API после запуска проекта можно посмотреть по адресам:
```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

### Автор
[Татьяна Шарова](https://github.com/TatianaSharova)