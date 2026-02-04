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

### Endpoint 1: Создание источника новостей

#### Тест 1 — успех (201 Created)

<img width="711" height="332" alt="image" src="https://github.com/user-attachments/assets/4e0b6cde-4424-477b-802f-c23b0cd7f48c" />

**Ответ:**

<img width="1101" height="219" alt="image" src="https://github.com/user-attachments/assets/72cc19e9-a44d-49f9-9a5b-dcf7adf5bfbb" />

**Код автотестов:**

```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response has id and created_at", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json).to.have.property("created_at");
});
```

**Результат автотестов**

<img width="410" height="251" alt="image" src="https://github.com/user-attachments/assets/4d57d8ae-1632-4999-b503-e8239f6273ae" />

#### Тест 2 — ошибка (422 Validation Error)

Body (не передаём обязательное поле `name`):

<img width="704" height="253" alt="image" src="https://github.com/user-attachments/assets/34ec5f66-0a8e-4a6a-83d4-9ceddfb740aa" />

**Ответ:**

<img width="1101" height="396" alt="image" src="https://github.com/user-attachments/assets/0c214c97-85f6-4e83-9daf-4e208b34698a" />


**Код автотестов:**

```javascript
pm.test("Status code is 422", function () {
    pm.response.to.have.status(422);
});
```

**Результат автотестов**

<img width="400" height="202" alt="image" src="https://github.com/user-attachments/assets/dfa0f703-0c51-46b4-843f-26208104eb40" />

### Endpoint 2: Получение списка источников

#### Тест 1 — успех (200 OK)

<img width="1017" height="660" alt="image" src="https://github.com/user-attachments/assets/ec8fe8c3-0b86-4f27-8dd6-b327ff8d4c0d" />

**Ответ:**

<img width="582" height="674" alt="image" src="https://github.com/user-attachments/assets/1264993b-4c69-4991-ac0c-4c09df7d61b1" />

**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is array", function () {
    pm.expect(pm.response.json()).to.be.an("array");
});
```

**Результат автотестов**

<img width="391" height="176" alt="image" src="https://github.com/user-attachments/assets/64a07d2a-5dc2-45f4-b72e-8c4a2a008347" />

#### Тест 2 — успех (пустой список)

(если источников ещё нет)

**Код автотестов:**

```javascript
pm.test("Empty array allowed", function () {
    pm.expect(pm.response.json()).to.be.an("array");
});
```

**Результат автотестов**

<img width="690" height="450" alt="image" src="https://github.com/user-attachments/assets/be8da4d5-c167-4843-bc22-8dce34f46890" />


### Endpoint 3: Получение источника по ID 

#### Тест 1 — успех (200 OK)

<img width="628" height="517" alt="image" src="https://github.com/user-attachments/assets/6da0ff16-637b-4feb-95f7-a45aa8f39951" />

**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Correct source returned", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json).to.have.property("name");
});
```

**Результат автотестов**

<img width="412" height="184" alt="image" src="https://github.com/user-attachments/assets/00aad3f6-7ded-452c-8f56-294beadf63f3" />


#### Тест 2 — ошибка (404 Not Found)

<img width="1015" height="431" alt="image" src="https://github.com/user-attachments/assets/dc8682cd-57e3-4ef6-9037-83267b70497a" />

**Код автотестов:**

```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});
```

**Результат автотестов**

<img width="401" height="133" alt="image" src="https://github.com/user-attachments/assets/a63c7060-0dde-4091-8f18-e04295f0ef9a" />

### Endpoint 4: Обновление источника

#### Тест 1 — успех (200 OK)

<img width="693" height="296" alt="image" src="https://github.com/user-attachments/assets/ad393c36-7790-4656-8a96-916028749beb" />

**Ответ:**

<img width="485" height="233" alt="image" src="https://github.com/user-attachments/assets/2282b9eb-d788-454e-8f30-ec1de78b92a1" />

**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Name updated", function () {
    pm.expect(pm.response.json().name).to.eql("BBC Updated");
});
```

**Результат автотестов**

<img width="399" height="183" alt="image" src="https://github.com/user-attachments/assets/0016778d-4da3-46fc-a833-665fd214d3eb" />


#### Тест 2 — ошибка (404)

<img width="1019" height="436" alt="image" src="https://github.com/user-attachments/assets/36ed1957-c9f7-4c60-8908-aa240bbdc764" />

### Endpoint 5: Удаление источника

#### Тест 1 — успех (200 OK)

<img width="1019" height="454" alt="image" src="https://github.com/user-attachments/assets/bdfe97fa-ffae-4632-aea9-0cf52abd5efc" />

**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Deleted status returned", function () {
    pm.expect(pm.response.json().status).to.eql("deleted");
});
```

**Результат автотестов**

<img width="263" height="99" alt="image" src="https://github.com/user-attachments/assets/92f15981-eb96-4d71-940f-423e932044c7" />


#### Тест 2 — ошибка (404)

<img width="1024" height="424" alt="image" src="https://github.com/user-attachments/assets/e7c3d785-fb5f-44ac-b952-f68d2007255d" />

### Endpoint 6: Создание новости

#### Тест 1 — успех (201 Created)

<img width="800" height="544" alt="image" src="https://github.com/user-attachments/assets/fadc3acc-90c1-406a-aa91-d2526644b0fd" />

**Код автотестов:**

```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("News created", function () {
    pm.expect(pm.response.json()).to.have.property("id");
});
```

**Результат автотестов**

<img width="227" height="138" alt="image" src="https://github.com/user-attachments/assets/46f55d57-dc70-4408-9fc2-fd44a0235278" />

#### Тест 2 — ошибка (404)

<img width="1021" height="523" alt="image" src="https://github.com/user-attachments/assets/229d5d9b-96c4-404d-a30a-ebd261432e1b" />

**Код автотестов:**

```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});
```
**Результат автотестов**

<img width="222" height="90" alt="image" src="https://github.com/user-attachments/assets/8b68c427-aff6-4a75-a494-a660d945f4f4" />


### Endpoint 7: Получение всех новостей

#### Тест 1 — успех (200)

<img width="824" height="652" alt="image" src="https://github.com/user-attachments/assets/b144f561-b456-4388-a0d1-b781def7776f" />


**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is array", function () {
    pm.expect(pm.response.json()).to.be.an("array");
});
```

**Результат автотестов**

<img width="272" height="157" alt="image" src="https://github.com/user-attachments/assets/5e2778c0-a71c-43b2-a251-d1201edeabd9" />

#### Тест 2 — ошибка (пустой список)

**Код автотестов:**

```javascript
pm.test("Empty list allowed", function () {
    pm.expect(pm.response.json()).to.be.an("array");
});
```

**Результат автотестов**

<img width="422" height="156" alt="image" src="https://github.com/user-attachments/assets/bf694bfb-3c28-4c35-9d8b-773518b91733" />


### Endpoint 8: Получение новости по ID

#### Тест 1 — успех (200)

<img width="871" height="634" alt="image" src="https://github.com/user-attachments/assets/80e5a3cc-c68b-4639-9c49-5247add18b2b" />

**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("News has title", function () {
    pm.expect(pm.response.json()).to.have.property("title");
});

```

**Результат автотестов**

<img width="417" height="170" alt="image" src="https://github.com/user-attachments/assets/7633a885-4bf5-4b42-829b-27a40c0cf412" />

#### Тест 2 — ошибка (404)

<img width="1018" height="423" alt="image" src="https://github.com/user-attachments/assets/a3df82a4-f0fc-44a1-b842-eafc66649d9b" />

**Код автотестов:**

```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});
```

**Результат автотестов**

<img width="427" height="141" alt="image" src="https://github.com/user-attachments/assets/d6f4598f-8ba9-4600-8320-812d1733c4b9" />

### Endpoint 9: Обновление новости

#### Тест 1 — успех

<img width="742" height="577" alt="image" src="https://github.com/user-attachments/assets/ef3b8352-c45a-45fc-b1cc-29f3621b388e" />


**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

**Результат автотестов**

<img width="828" height="469" alt="image" src="https://github.com/user-attachments/assets/c9a7a74f-df47-4195-8c4e-532a8a1c350a" />

#### Тест 2 — ошибка (404)

<img width="1025" height="465" alt="image" src="https://github.com/user-attachments/assets/a843c2eb-c89c-4faf-add2-26bae92fab1d" />

**Код автотестов:**

```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});
```

**Результат автотестов**

<img width="800" height="457" alt="image" src="https://github.com/user-attachments/assets/78573ca0-7839-4381-ac7f-1a2d1449e6b0" />

### Endpoint 10: Удаление новости

#### Тест 1 — успех

<img width="768" height="533" alt="image" src="https://github.com/user-attachments/assets/c64b3226-dab8-4814-85df-5747b079aa2d" />

**Код автотестов:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

**Результат автотестов**

<img width="483" height="154" alt="image" src="https://github.com/user-attachments/assets/9049d278-c11f-4fcf-a8ef-dd697c7a9e25" />


#### Тест 2 — ошибка (404)

<img width="760" height="523" alt="image" src="https://github.com/user-attachments/assets/e5252db0-2c7b-4f7b-98f9-b9240a4fe165" />


**Код автотестов:**

```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});
```

**Результат автотестов**

<img width="438" height="147" alt="image" src="https://github.com/user-attachments/assets/f5092b18-1e6a-4672-bc32-6ebacab25a2d" />
