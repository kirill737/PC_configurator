# PostgresSQL
1. Скачиваешь PostgresSQL
2. Создание бдхи

1) Заходишь под главным пользователем -> postgres
В обычном терминале WSL:
```
sudo -u postgres psql
```
2) Cоздаёшь пользователя с такими же параметрами как у меня 
Это уже в psql-ом терминале (<user>=# ...)
```
CREATE DATABASE pc_config_db;
```
2) Cоздаёшь бдху 
```
CREATE DATABASE pc_config_db;
```
3) Cоздаёшь пользователя с такими же параметрами как у меня 
```
CREATE USER kirill WITH PASSWORD 'root';
```
4) Выдаёшь своему пользователю права для бдхи
```
GRANT ALL PRIVILEGES ON DATABASE my_datapc_config_dbbase TO kirill
```
5) Всё, можно выходить из psql
```
\q
```
3. Скачиваем всю муть для работы
1) Скачиваешь в VS Code расширения:
- "SQLTools"
- "SQLTools PostgreSQL/Cockroach Driver"
вроде только этих хватит
2) Появится после этого справа в менюхе кнопка с бдхой. Заходишь туда
3) Создаёшь подключение
4) Заполняешь всё что нужно о пользователе и бдхе:
user: kirill
db: pc_config_db
localhost: 5432
и т.д.
5) Подключаешься
4. Заполнение бдхи таблицами
Теперь по идеи можно просто запустить 2 файлика из папки sql_scripts
1) create_types.sql
2) create_all.sql
Если нет ошибок, то ты молодец, и всё сработало. Можешь протестить селектом
5. Дальше надо заполнить тестовыми данными
1) По сути, просто запусти питоновский файл (кстати да, питон вроде нужен минимум 3.11)
```
python3.11 test.py
```
2) Всё, теперь проверь селектами снова чо как вышло (писать запросы советую в файле sql_scripts/manual.sql, я его для временных команд и сделал)

# Redis
1. Скачиваешь (вроде так)
```
sudo apt-get install redis-server -y
```
2. Запускаешь
```
service redis-server start
```
3. ВСЁ - МОЖНО ЗАПУСКАТЬ САЙТ
(в venv не забудь зайти)
```
python3.11 main.py
```



# PostgreSQL
## 1. users - Пользователи
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – имя пользователя
- **email** (varchar, unique) – email пользователя
- **password_hash** (varchar) – хеш пароля
- **role** (enum: 'admin', 'user', 'guest') – роль пользователя
- **created_at** (timestamp) – дата регистрации

## 2. builds - Сборки
- **id** (PK, serial) – уникальный идентификатор
- **user_id** (FK → users.id) – владелец сборки
- **name** (varchar) – название сборки
- **description** (text) – описание сборки
- **created_at** (timestamp) – дата создания
- **image_path** (varchar) - путь к фото сборки

## 3. compnents
- **id** (PK, serial) – уникальный идентификатор
- **type** (varchar) 
- **price** (decimal)
- **created_at** (timestamp)

```sql
CREATE TABLE components (
    id SERIAL PRIMARY KEY,
    type VARCHAR NOT NULL CHECK (type IN (
        'cpu',
        'motherboard',
        'gpu',
        'ram',
        'storage',
        'power_supply',
        'case',
        'mice',
        'headphones',
        'microphone',
        'monitor'
        )
    ),
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```
## 4. build_components
- **id** (PK, serial) – уникальный идентификатор
- **build_id**
- **component_id**
- **amount**

## 5. cpus - Процессоры
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – название процессора
- **brand** (varchar) – производитель (Intel, AMD)
- **cores** (int) – количество ядер
- **threads** (int) – количество потоков
- **base_clock** (decimal) – базовая частота (ГГц)
- **boost_clock** (decimal) – максимальная частота (ГГц)
- **socket** (varchar) – сокет
- **tdp** (int) – тепловыделение (Вт)

## 6. motherboards - Материнки
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – название материнской платы
- **brand** (varchar) – производитель
- **socket** (varchar) – поддерживаемый сокет
- **chipset** (varchar) – чипсет
- **form_factor** (varchar) – форм-фактор (ATX, Micro-ATX и т. д.)
- **ram_slots** (int) – количество слотов для ОЗУ
- **max_ram** (int) – максимальный объём ОЗУ (ГБ)
- **m2_slots** (int) – количество M.2 слотов

## 7. gpus - Видеокарты
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – название видеокарты
- **brand** (varchar) – производитель (NVIDIA, AMD, Intel)
- **memory_size** (int) – объём памяти (ГБ)
- **memory_type** (varchar) – тип памяти (GDDR6, GDDR5 и т. д.)
- **core_clock** (decimal) – частота ядра (МГц)
- **boost_clock** (decimal) – максимальная частота (МГц)
- **tdp** (int) – тепловыделение (Вт)
- **interface** (varchar) – интерфейс (PCIe 4.0 и т. д.)

## 8. rams - Оперативка
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – название оперативной памяти
- **brand** (varchar) – производитель
- **capacity** (int) – объём одной планки (ГБ)
- **type** (varchar) – тип (DDR4, DDR5 и т. д.)
- **speed** (int) – частота (МГц)
- **cas_latency** (int) – задержка CAS

## 9. storages - Диски
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – название накопителя
- **brand** (varchar) – производитель
- **type** (varchar) – тип накопителя (SSD, HDD)
- **capacity** (int) – объём памяти (ГБ)
- **interface** (varchar) – интерфейс (SATA, NVMe и т. д.)
- **read_speed** (int) – скорость чтения (МБ/с)
- **write_speed** (int) – скорость записи (МБ/с)

## 10. power_supplies - Блок питания
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – название блока питания
- **brand** (varchar) – производитель
- **wattage** (int) – мощность (Вт)
- **efficiency_rating** (varchar) – сертификация (80 Plus Bronze, Gold и т. д.)
- **modular** (boolean) – модульность (true/false)

## 11. cases - Корпус
- **id** (PK, serial) – уникальный идентификатор
- **name** (varchar) – название корпуса
- **brand** (varchar) – производитель
- **form_factor** (varchar) – совместимость (ATX, Micro-ATX и т. д.)
- **max_gpu_length** (int) – максимальная длина видеокарты (мм)
- **max_cpu_cooler_height** (int) – максимальная высота кулера (мм)
- **max_psu_length** (int) – максимальная длина БП (мм)

## 12. mice (PostgreSQL)
- **id** (PK, serial) – уникальный идентификатор
<!-- - **user_id** (FK → users.id) – владелец -->
- **name** (varchar) – название модели
- **brand** (varchar) – производитель
- **dpi** (int) – максимальное разрешение DPI
- **connection_type** (varchar) – тип подключения (проводная, беспроводная)
- **buttons** (int) – количество кнопок
- **weight** (decimal) – вес (граммы)
- **rgb** (boolean) – наличие RGB-подсветки

## 13. keyboards (PostgreSQL)
- **id** (PK, serial) – уникальный идентификатор
<!-- - **user_id** (FK → users.id) – владелец -->
- **name** (varchar) – название модели
- **brand** (varchar) – производитель
- **switch_type** (varchar) – тип переключателей (мембранные, механические, оптические)
- **connection_type** (varchar) – тип подключения (проводная, беспроводная)
- **layout** (varchar) – раскладка (ANSI, ISO, JIS)
- **rgb** (boolean) – наличие RGB-подсветки
- **num_pad** (boolean) – наличие цифрового блока

## 14. headphones
- **id** (PK, serial) – уникальный идентификатор
<!-- - **user_id** (FK → users.id) – владелец -->
- **name** (varchar) – название модели
- **brand** (varchar) – производитель
- **type** (varchar) – тип (накладные, внутриканальные, полноразмерные)
- **connection_type** (varchar) – тип подключения (проводные, беспроводные)
- **frequency_range** (varchar) – диапазон частот (20Hz - 20kHz)
- **impedance** (int) – сопротивление (Ом)
- **microphone** (boolean) – наличие встроенного микрофона
- **rgb** (boolean) – наличие RGB-подсветки

## 15. microphones
- **id** (PK, serial) – уникальный идентификатор
<!-- - **user_id** (FK → users.id) – владелец -->
- **name** (varchar) – название модели
- **brand** (varchar) – производитель
- **connection_type** (varchar) – тип подключения (USB, XLR, 3.5mm)
- **directionality** (varchar) – направленность (кардиоидный, всенаправленный и т. д.)
- **sample_rate** (int) – частота дискретизации (Гц)
- **bit_depth** (int) – битовая глубина (бит)

## 16. monitors (PostgreSQL)
- **id** (PK, serial) – уникальный идентификатор
<!-- - **user_id** (FK → users.id) – владелец -->
- **name** (varchar) – название модели
- **brand** (varchar) – производитель
- **screen_size** (decimal) – диагональ экрана (дюймы)
- **resolution** (varchar) – разрешение (1920x1080, 2560x1440 и т. д.)
- **refresh_rate** (int) – частота обновления (Гц)
- **panel_type** (varchar) – тип матрицы (IPS, VA, TN)
- **response_time** (decimal) – время отклика (мс)
- **g_sync** (boolean) – поддержка G-Sync
- **freesync** (boolean) – поддержка FreeSync

## 17. wishlists
- **id** (PK, serial) – уникальный идентификатор
- **user_id** (FK → users.id) – владелец
- **name** (varchar) – название вишлиста
- **created_at** (timestamp) – дата создания

# 18. wishlist_items
- **id** (PK, serial) – уникальный идентификатор
- **wishlist_id** (FK → wishlists.id) – ссылка на вишлист
- **component_type** (varchar) – тип компонента
- **component_id** (int) – ID компонента (связывается динамически)

# MongoDB
## 19. posts
- **_id** (ObjectId) – уникальный идентификатор
- **user_id** (ObjectId) – автор поста
- **title** (string) – заголовок поста
- **content** (string) – содержание
- **created_at** (datetime) – дата создания
- **likes** (array) – массив ID пользователей, поставивших лайк
- **comments** (array) – массив объектов комментариев

## 20. comments
- **_id** (ObjectId) – уникальный идентификатор
- **post_id** (ObjectId) – ID поста
- **user_id** (ObjectId) – автор комментария
- **text** (string) – текст комментария
- **created_at** (datetime) – дата создания

# Redis
## 21. user_sessions
- **session_id** (string, ключ) – уникальный идентификатор сессии
- **user_id** (int) – ID пользователя
- **expires_at** (timestamp) – время истечения сессии

## 22. recent_views
- **user_id** (ключ) – ID пользователя
- **viewed_items** (list) – список недавно просмотренных компонентов (ограниченный, например, 10 записями)
