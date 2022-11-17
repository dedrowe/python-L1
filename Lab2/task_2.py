import csv
import os
import logging
from datetime import datetime
import re

logger = logging.getLogger()
logger.setLevel('INFO')


def write_data_to_file(data: list, destination: str) -> None:
    """
    Функция принимает на вход список данных и записывает их в выбранный файл
    :param data: Список с данными
    :param destination: Путь к файлу, в который необходимо записать данные
    :return: Функция не возвращает значение
    """
    try:
        with open(destination, 'w') as f:
            for i in data:
                writer = csv.writer(f, dialect='unix')
                writer.writerow(i)
    except OSError as er:
        logging.warning(f'Ошибка открытия файла {er}')


def create_list(source: str = "dataset.csv", last_date: str = "1992-07-01", dest: str = 'task_2') -> None:
    """
    Функция создает список данных из файла
    :param source: Файл, из которого программа считывает данные
    :param last_date: Последняя дата в файле
    :param dest: Путь к файлу
    :return: Фукнция не возвращает значение
    """
    try:
        with open(source, 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            rows = [next(reader)]
            for row in reader:
                if rows[-1][0][:4] != row[0][:4]:
                    logging.info(f'Программа сейчас на дате: {row[0]}, '
                                 f'последняя дата: {last_date}')
                    temp_date = re.sub(r'-', '', rows[-1][0])
                    temp_last_date = re.sub(r'-', '', rows[0][0])
                    path = f'{dest}/{temp_date}_' \
                           f'{temp_last_date}'
                    write_data_to_file(rows, path)
                    rows = [row]
                else:
                    rows.append(row)
            temp_date = re.sub(r'-', '', rows[-1][0])
            temp_last_date = re.sub(r'-', '', rows[0][0])
            path = f'{dest}/{temp_date}_' \
                   f'{temp_last_date}'
            write_data_to_file(rows, path)
    except OSError as er:
        logging.warning(f'Ошибка открытия файла {er}')


if __name__ == "__main__":
    try:
        os.makedirs('task_2')
        logging.info('Папка успешно создана')
        create_list()
    except OSError as er:
        logging.info(f'Ошибка при создании папки {er}')
