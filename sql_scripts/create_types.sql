CREATE TYPE USER_ROLE AS ENUM ('user', 'admin', 'guest');
CREATE TYPE COMPONENT AS ENUM (
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
);

CREATE TYPE CONNECTION_TYPE AS ENUM ('wireless', 'wired');

CREATE TYPE KEYBOARD_LAYOUT AS ENUM (
    '100%',
    '80%',
    '75%',
    '65%',
    '60%',
    '40%',
    'not standart'
);

