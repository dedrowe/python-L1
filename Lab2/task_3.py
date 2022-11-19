import csv
import logging
import os
from datetime import datetime
import re


logger = logging.getLogger()
logger.setLevel('INFO')


def write_data_to_file(data: list, destination: str) -> None:
    """
    Функция принимает список и путь к файлу, записывает в этот файл полученный список
    :param data: Список для записи в файл
    :param destination: Путь к файлу в который производится запись
    :return: Функция не возвращает значение
    """
    try:
        with open(destination, 'w') as f:
            for i in data:
                writer = csv.writer(f, dialect='unix')
                writer.writerow(i)
    except OSError as er:
        logging.warning(f'Ошибка открытия файла {er}')


def create_list(source: str = 'dataset.csv', last_date: str = "1992-07-01", dest: str = 'task_3') -> None:
    """
    Функция считывает данные за неделю и превращает их в список
    :param source: Файл из которого считываются данные
    :param last_date: Последняя дата в файле
    :param dest: Путь к файлу
    :return: Функция не возвращает значение
    """
    with open(source, 'r') as dataset:
        reader = csv.reader(dataset, dialect='unix')
        rows = [next(reader)]
        for row in reader:
            logging.info(f'Программа сейчас на дате: {row[0]}, '
                         f'последняя дата: {last_date}')
            if datetime.date(datetime.strptime(rows[-1][0], "%Y-%m-%d")).isocalendar()[1] == \
                    datetime.date(datetime.strptime(row[0], "%Y-%m-%d")).isocalendar()[1]:
                rows.append(row)
            else:
                temp_date = re.sub(r'-', '', rows[-1][0])
                temp_last_date = re.sub(r'-', '', rows[0][0])
                path = os.path.join(dest, f'{temp_date}_{temp_last_date}')
                write_data_to_file(rows, path)
                rows = [row]
        temp_date = re.sub(r'-', '', rows[-1][0])
        temp_last_date = re.sub(r'-', '', rows[0][0])
        path = os.path.join(dest, f'{temp_date}_{temp_last_date}')
        write_data_to_file(rows, path)


if __name__ == "__main__":
    try:
        os.makedirs('task_3')
        logging.info('Папка успешно создана')
        create_list()
    except OSError as er:
        logging.info(f'Ошибка при создании папки {er}')
