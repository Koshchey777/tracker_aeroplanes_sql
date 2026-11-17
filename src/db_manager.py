import psycopg2

from config import db_config


class DBManager:
    """Класс для работы с данными"""

    def __init__(self, dbname):
        """Инициализация с помощью имени базы"""
        self.__dbname = dbname

    def __execute_query(self, query, params=None):
        """Функция для подключения к базе для реализации запроса"""
        if params is None:
            params = ()
        with psycopg2.connect(dbname=self.__dbname, **db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                data = cursor.fetchall()
        return data

    def get_countries_and_aeroplanes_count(self):
        """Показывает количество самолетов в
        воздушных пространствах стран"""
        query = """SELECT c.country, COUNT(a.ica)
        FROM countries c
        JOIN airplanes a ON c.id = a.country_id
        GROUP BY c.country
        """
        return self.__execute_query(query)

    def get_all_aeroplanes(self):
        """Функция выводит список самолетов"""
        query = """SELECT a.ica, a.callsign, a.altitude, a.on_ground, a.velocity, c.country FROM airplanes a
        JOIN countries c ON c.id = a.country_id
        ORDER BY c.country"""
        return self.__execute_query(query)

    def get_avg_speed(self):
        """Функция возвращает среднюю скорость среди самолетов"""
        query = """SELECT AVG(velocity) FROM airplanes"""
        data = self.__execute_query(query)
        return data

    def get_avg_height(self):
        """Функция возвращает среднюю высоту среди самолетов"""
        query = """SELECT AVG(altitude) FROM airplanes"""
        data = self.__execute_query(query)
        return data

    def aeroplanes_with_higher_speed(self):
        """Функция возвращает список самолетов,
        у которых скорость выше средней"""
        query = """SELECT a.ica, a.callsign, a.altitude, a.on_ground, a.velocity, c.country FROM airplanes a
        JOIN countries c ON c.id = a.country_id
        WHERE a.velocity > (SELECT AVG(velocity) FROM airplanes)
        ORDER BY c.country"""
        return self.__execute_query(query)

    def get_aeroplanes_with_keyword(self, word):
        """Функция для поиска в позывном самолета"""
        query = f"""SELECT a.ica, a.callsign, a.altitude, a.on_ground, a.velocity, c.country FROM airplanes a
        JOIN countries c ON c.id = a.country_id
        WHERE a.callsign ILIKE %s
        ORDER BY c.country"""
        search = f"%{word}%"
        return self.__execute_query(query, (search,))
