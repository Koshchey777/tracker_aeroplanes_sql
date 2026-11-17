from src.db_manager import DBManager
from src.utils_db import create_database, create_tables, insert_data, get_data_api


def print_countries_count(data):
    """Функция форматирует данные о странах и количестве самолётов"""
    res = ""
    for country, count in data:
        res += f"Страна: {country}. Количество самолетов: {count}\n"
    return res


def print_airplanes_list(data):
    """Функция форматирует список самолётов"""
    res = ""
    for ica, callsign, altitude, on_ground, velocity, country in data:
        res += f"Идентификатор: {ica}. Позывной: {callsign}. Высота: {altitude}. На земле: {on_ground}. Скорость: {velocity} Страна: {country}\n"
    return res


def main():
    """Функция запуска приложения"""
    db_name = "air"
    create_database(db_name)
    create_tables(db_name)
    data = get_data_api()
    insert_data(db_name, data)

    db_manager = DBManager(db_name)

    print("Приветствую! Трекер самолётов готов к работе.")
    print("")
    print("Выберите действие:")
    print("1) Получить количество самолетов в воздушных пространствах стран")
    print("2) Получить список самолетов")
    print("3) Получить среднюю скорость среди самолетов")
    print("4) Получить среднюю высоту среди самолетов")
    print("5) Получить список самолетов, чья скорость выше средней")
    print("6) Найти самолет по символам в его позывном")
    print("""7) Выход
    
    """)

    while True:
        answer = input()

        if answer == "1":
            print(
                print_countries_count(db_manager.get_countries_and_aeroplanes_count())
            )

        elif answer == "2":
            print(print_airplanes_list(db_manager.get_all_aeroplanes()))

        elif answer == "3":
            print(f'Cредняя скорость: {round(db_manager.get_avg_speed()[0][0], 2)}')

        elif answer == "4":
            print(f'Cредняя высота: {round(db_manager.get_avg_height()[0][0], 2)}')

        elif answer == "5":
            print(print_airplanes_list(db_manager.aeroplanes_with_higher_speed()))

        elif answer == "6":
            print("Введите строку для поиска:")
            str_for_get = input()
            data = db_manager.get_aeroplanes_with_keyword(str_for_get)
            if not data:
                print("По данному запросу совпадений нет.")
            else:
                print(print_airplanes_list(data))

        elif answer == "7":
            print("Окончание работы программы.")
            break

        else:
            print("Введено некорректное значение. Попробуйте еще раз")


if __name__ == "__main__":
    main()
