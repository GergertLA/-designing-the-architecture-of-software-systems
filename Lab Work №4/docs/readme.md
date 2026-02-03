# Лабораторная работа №4

**Тема:** Проектирование REST API

**Цель работы:** Получить опыт проектирования программного интерфейса.

В рамках лабораторной работы реализуется REST API сервиса управления источниками новостей и результатами анализа новостей, используемого в системе анализа тональности новостей и их влияния на цену криптовалют.

API предоставляет возможность:
- управлять списком новостных источников;
- получать и сохранять результаты анализа новостей;
- обновлять и удалять данные.

### Принятые проектные решения при проектировании API

#### 1. Использование REST-подхода
API спроектирован в соответствии с REST-принципами: каждая сущность представлена как ресурс, доступ к которому осуществляется через уникальный URL, а операции над ресурсами выполняются с помощью стандартных HTTP-методов.

#### 2. Использование стандартных HTTP-методов
Для работы с ресурсами применяются общепринятые методы:
- GET — получение данных
- POST — создание новых сущностей
- PUT — обновление существующих сущностей
- DELETE — удаление сущностей  

Это упрощает понимание API и делает его предсказуемым.

#### 3. Ресурсно-ориентированные URL
URL описывают сущности системы (sources, articles, sentiments), а не действия над ними. Например, `/api/sources`, а не `/api/getSources`.

#### 4. Формат обмена данными JSON
Все входные и выходные данные передаются в формате JSON, так как он является простым, читаемым и поддерживается большинством клиентов и инструментов тестирования.

#### 5. Явное описание структуры запросов и ответов
Для каждого эндпоинта зафиксированы входные параметры и формат ответа, что упрощает использование API и снижает вероятность ошибок при интеграции.

#### 6. Использование HTTP-кодов ответа
API возвращает стандартные HTTP-коды (200, 201, 400, 404), что позволяет клиенту корректно интерпретировать результат запроса без анализа тела ответа.

#### 7. Минимально необходимый набор полей (YAGNI)
В запросах и ответах используются только те поля, которые реально нужны для текущих сценариев использования. Избыточные и «на будущее» поля не добавлялись.

#### 8. Отсутствие бизнес-логики на клиенте
API выполняет только операции управления данными. Клиент (Grafana) работает напрямую с БД и не содержит собственной логики, что упрощает архитектуру.

---
## Документация по API

### 1. Создание источника новостей

**POST** `/api/v1/sources`

Создаёт новый источник новостей, который будет использоваться парсером для сбора данных.

**Request body**

```json
{
  "name": "string",
  "url": "string",
  "type": "string"
}
```

**Responses**

- 201 Successful Response

```json
{
  "name": "string",
  "url": "string",
  "type": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2026-01-29T05:08:56.411Z"
}
```
- 422 Validation Error

```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### 2. Получение списка источников
**GET** `/api/v1/sources`

Возвращает список всех зарегистрированных источников новостей.

**Responses**

- 200 Successful Response
```json
[
  {
    "name": "string",
    "url": "string",
    "type": "string",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2026-01-29T05:05:55.038Z"
  }
]
```

### 3. Получение новости по идентификатору

**GET** `/api/v1/source/{source_id}`

Возвращает новость с результатом анализа тональности.

**Parameters**

- source_id "string"

**Responses**

- 200 Successful Response

```json
{
  "name": "string",
  "url": "string",
  "type": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2026-01-29T05:10:16.877Z"
}
```

- 422 Validation Error

```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### 4. Создание новости (внутренний API парсера)

**POST** `/api/v1/news`

Используется парсером для сохранения загруженной новости и результата анализа тональности.

**Request body**

```json
{
  "title": "string",
  "content": "string",
  "sentiment": 0,
  "source_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "published_at": "2026-01-29T05:12:42.887Z"
}
```

**Responses**

- 201 Successful Response
```json
"string"
```

- 422 Validation Error
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### 5. Обновление источника новостей
**PUT** `/api/v1/sources/{source_id}`

Обновляет параметры существующего источника новостей.

**Parameters**

- source_id "string"

**Request body**
```json
{
  "name": "string",
  "url": "string",
  "type": "string"
}
```

**Responses**

- 200 Successful Response
```json
{
  "name": "string",
  "url": "string",
  "type": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2026-01-29T05:14:07.515Z"
}
```

- 422 Validation Error
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### 6. Удаление источника новостей

**DELETE** `/api/v1/sources/{source_id}`

Удаляет источник новостей и связанные с ним данные.

**Parameters**

- source_id "string"

**Responses**

- 200 Successful Response
```json
"string"
```

- 422 Validation Error
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## Тестирование API

### Endpoint 1: Создание источника
#### Тест 1 — успешное создание

**Метод:** `POST`

**URL:** `{{base_url}}/api/v1/sources`

**Body:**
```json
{
  "name": "CoinDesk",
  "url": "https://coindesk.com",
  "type": "rss"
}
```
<img width="1280" height="467" alt="image" src="https://github.com/user-attachments/assets/c31f85ff-3da9-45a8-8b1b-c6af1d50c83f" />
<img width="1280" height="459" alt="image" src="https://github.com/user-attachments/assets/aead0735-8554-4306-aed7-8f79dad5f109" />

**Ожидаемый ответ:**
- 201 Created
- JSON с id и created_at

**Tests**
```javascript
pm.test("Status 201", () => {
    pm.response.to.have.status(201);
});

pm.test("Response contains id", () => {
    pm.expect(pm.response.json()).to.have.property("id");
});
```

<img width="1280" height="483" alt="image" src="https://github.com/user-attachments/assets/cd1b729b-8020-4626-9bc2-9011488702a5" />

❌ Тест 2 — ошибка валидации

**Body:** `{}`


**Ожидаемый ответ:**
- 422 Unprocessable Entity

**Tests:**
```javascript
pm.test("Validation error", () => {
    pm.response.to.have.status(422);
});
```
<img width="1740" height="810" alt="image" src="https://github.com/user-attachments/assets/1602aac5-5628-4fe3-910e-8f2636c539ac" />
<img width="1746" height="448" alt="image" src="https://github.com/user-attachments/assets/25bc41ef-75b5-4143-a003-b6365bd3391e" />

### Endpoint 2: Получить все источники
#### Тест 1 — список источников

**Метод:** `GET`
**URL:** `{{base_url}}/api/v1/sources`

**Ожидаемый ответ:**
- 200 OK
- Массив

**Tests**
```json
pm.test("Status 200", () => {
    pm.response.to.have.status(200);
});

pm.test("Response is array", () => {
    pm.expect(pm.response.json()).to.be.an("array");
});
```

<img width="1361" height="778" alt="image" src="https://github.com/user-attachments/assets/6ecb812c-e1e1-42de-993a-51842237f98e" />
<img width="1371" height="559" alt="image" src="https://github.com/user-attachments/assets/fcf7a676-8e32-4c64-b2a2-c82f90262ff8" />



<
По каждому реализуемому API предоставить следующую информацию: 
- Тестируемое API.
- Метод.
- Строка запроса, используемая для тестирования. Можно представить в виде текстовой строки или принтскрина из Postman, чтобы продемонстрировать все передаваемые данные.
- Принтскрин из Postman передаваемых заголовков и параметров (Params, Authorization, Headers, Body).
- Принтскрины из Postman полученного ответа (Body и Headers).
- Код автотестов (на получение возвращаемого статуса и содержимого ответа).
- Принтскрины из Postman результатов тестирования (Test Results).
>


-- возвращение статуса + любая ошибка
-- возможно использовать автогенерацию тестов
