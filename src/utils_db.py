import psycopg2

from config import db_config, COUNTRIES
from src.api_adapter import NominatimApi, OpenskyApi


def create_database(namedb):
    '''Создание базы данных'''
    conn = psycopg2.connect(dbname='postgres', **db_config)
    cursor = conn.cursor()
    conn.autocommit = True

    cursor.execute(f'DROP DATABASE IF EXISTS {namedb}')
    cursor.execute(f'CREATE DATABASE {namedb}')

    cursor.close()
    conn.close()


def create_tables(namedb):
    '''Создание таблицы с данными о странах
    и таблицы с данными о самолетах'''
    with psycopg2.connect(dbname=namedb, **db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255) NOT NULL UNIQUE,
            lamin FLOAT,
            lamax FLOAT,    
            lomin FLOAT,
            lomax FLOAT
            )'''
                           )

            cursor.execute('''CREATE TABLE IF NOT EXISTS airplanes (
            ica VARCHAR(50) PRIMARY KEY,
            callsign VARCHAR(50),
            altitude FLOAT,
            velocity FLOAT,
            on_ground BOOLEAN,
            country_id INT REFERENCES countries(id)
            )''')


def insert_data(namedb):
    '''Заполнение таблиц countries и airplanes данными,
    полученными от API'''
    with psycopg2.connect(dbname=namedb, **db_config) as conn:
        with conn.cursor() as cursor:
            for country in COUNTRIES:
                nominatium = NominatimApi(country)
                bbox = nominatium.get_data()
                lamin, lamax, lomin, lomax = bbox
                cursor.execute('''INSERT INTO countries (country, lamin, lamax, lomin, lomax) VALUES (%s, %s, %s, %s, %s)
                RETURNING id''', (country, lamin, lamax, lomin, lomax))
                country_db_id = cursor.fetchone()[0]
                opensky_api = OpenskyApi(bbox)
                for airplane in opensky_api.get_data():
                    ica = airplane['ica']
                    callsign = airplane['callsign']
                    altitude = airplane['altitude']
                    on_ground = airplane['on_ground']
                    velocity = airplane['velocity']
                    cursor.execute('''INSERT INTO airplanes (ica, callsign, altitude, on_ground, velocity, country_id) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ica) DO UPDATE SET
                    callsign = EXCLUDED.callsign,
                    altitude = EXCLUDED.altitude,
                    on_ground = EXCLUDED.on_ground,
                    velocity = EXCLUDED.velocity''', (ica, callsign, altitude, on_ground, velocity, country_db_id))

db_name = 'air'
create_database(db_name)
create_tables(db_name)
insert_data(db_name)
