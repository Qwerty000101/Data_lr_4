#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Для своего варианта лабораторной работы 2.17 добавьте
# возможность получения имени файла данных, используя
# соответствующую переменную окружения.


import argparse
import json
import sys
import os.path


# Вариант 29
def add_route(staff, start, end, number):
    '''
    Добавить маршрут
    '''
    staff.append({
        'name_start': start,
        'name_end': end,
        'number': number
    })
    return staff


def list(routes):
    '''
    Вывести список маршрутов
    '''
    if routes:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 30,
            '-' * 8
        )
        print(line)

        print('| {:^4} | {:^30} | {:^30} | {:^8} |'.format(
            "№",
            "Начальный пункт",
            "Конечный пункт",
            "Номер"
        )
        )
        print(line)

        for idx, route in enumerate(routes, 1):
            print('| {:>4} | {:<30} | {:<30} | {:>8} |'.format(
                idx,
                route.get('name_start', ''),
                route.get('name_end', ''),
                route.get('number', 0)
            )
            )
            print(line)
    else:
        print("Список маршрутов пуст.")


def save_routes(file_name, staff):
    """
    Сохранить все маршруты в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузить все маршруты из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def select_routes(routes, command):
    '''
    Вывести выбранные маршруты
    '''
    station = command
    count = 0

    for route in routes:
        if (station.lower() == route["name_start"].lower() or
                station == route["name_end"].lower()):

            count += 1
            print('{:>4}: {}-{}, номер маршрута: {}'.format(count,
                  route["name_start"], route["name_end"], route["number"]))

    if count == 0:
        print("Маршрут не найден.")


def main(command_line=None):
    '''
    Основная функция
    '''
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-f",
        "--filename",
        required=False,
        action="store",
        help="The data file name"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("routes")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления маршрута.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new route"
    )
    add.add_argument(
        "-s",
        "--start",
        action="store",
        required=True,
        help="Start position on route"
    )
    add.add_argument(
        "-e",
        "--end",
        action="store",
        help="End position on route"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        type=int,
        required=True,
        help="Number of route"
    )
    # Создать субпарсер для отображения всех маршрутов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all routes"
    )
    # Создать субпарсер для выбора маршрутов.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the routes"
    )
    select.add_argument(
        "-t",
        "--station",
        action="store",
        type=str,
        required=True,
        help="Routes with this station"
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    os.environ.setdefault("LAB4", "C:/Users/HAIER/Desktop/Задания/" +
                          "Анализ данных/Data_lr_4/data/routes.json")
    file_name = args.filename
    if not file_name:
        file_name = os.environ.get("LAB4")
    if not file_name:
        print("Data file name not set in env variable", file=sys.stderr)
        sys.exit(1)

    # Загрузить все маршруты из файла, если файл существует.
    is_dirty = False
    if os.path.exists(file_name):
        routes = load_routes(file_name)
    else:
        routes = []
    # Добавить маршрут.
    if args.command == "add":
        if(routes is None):
            routes = []
        routes = add_route(
            routes,
            args.start,
            args.end,
            args.number
        )
        is_dirty = True
    # Отобразить все маршруты.
    elif args.command == "display":
        list(routes)

    # Выбрать требуемые маршруты.
    elif args.command == "select":
        select_routes(routes, args.station)
        print(args.station)
    # Сохранить данные в файл, если список маршрутов был изменен.
    if is_dirty:
        save_routes(file_name, routes)


if __name__ == '__main__':
    main()


