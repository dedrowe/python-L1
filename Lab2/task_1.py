import csv
import os
import logging

logger = logging.getLogger()
logger.setLevel('INFO')


def parse_data(data: str) -> None:
    """
    Функция превращает полученную строку в список
    :param data: Строка, которую функция разбивает
    :return: Функция не возвращает значение
    """
    split_data = data.split(sep=', ')
    write_data_to_file('task_1/X.csv', split_data[0])
    write_data_to_file('task_1/Y.csv', split_data[1])


def write_data_to_file(source: str, value: str) -> None:
    """
    Функция заисывает полученную строку в выбранный файл
    :param source: Строка, которую функция записывает в файл
    :param value: Файл, в который фунция записывает строку
    :return: Функция не возвращает значение
    """
    try:
        with open(source, 'w') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow({value})
    except OSError:
        logging.warning('Ошибка открытия файла')


def read_data_from_file(source: str = "dataset.csv", last_row: str = "1992-07-01, 125.26") -> None:
    """
    Фукнция считывает данные из файла
    :param source: Файл из которого происходит считывание данных
    :param last_row: Строка, до которой функция будет считывать данные
    :return: Фукнция не возвращает никакое значения
    """
    try:
        with open(source, 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            row = next(reader)[0]
            while row != last_row:
                logging.info(f'Программа сейчас на дате: {row.split(sep=", ")[0]}, '
                             f'последняя дата: {last_row.split(sep=", ")[0]}')
                parse_data(row)
                row = next(reader)[0]
            parse_data(row)
    except OSError:
        logging.warning('Ошибка открытия файла')


if __name__ == "__main__":
    try:
        os.makedirs('task_1')
        logging.info('Папка успешно создана')
        read_data_from_file()
    except OSError:
        logging.warning('Ошибка при создании папки')
