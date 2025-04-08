1. Создаются комплектующие 
2. 



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
