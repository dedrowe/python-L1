import csv
import os
import logging

logger = logging.getLogger()
logger.setLevel('INFO')


def parse_data(data: list) -> None:
    """
    Функция превращает полученную строку в список
    :param data: Строка, которую функция разбивает
    :return: Функция не возвращает значение
    """
    write_data_to_file('task_1/X.csv', data[0])
    write_data_to_file('task_1/Y.csv', data[1])


def write_data_to_file(source: str, value: str) -> None:
    """
    Функция заисывает полученную строку в выбранный файл
    :param source: Строка, которую функция записывает в файл
    :param value: Файл, в который фунция записывает строку
    :return: Функция не возвращает значение
    """
    try:
        with open(source, 'a') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow({value})
    except OSError:
        logging.warning('Ошибка открытия файла')


def read_data_from_file(source: str = "dataset.csv", last_date: str = "1992-07-01") -> None:
    """
    Фукнция считывает данные из файла
    :param source: Файл из которого происходит считывание данных
    :param last_date: Последняя дата в файле
    :return: Фукнция не возвращает никакое значения
    """
    try:
        with open(source, 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            for row in reader:
                parse_data(row)
                logging.info(f'Программа сейчас на дате: {row[0]}, '
                             f'последняя дата: {last_date}')
    except OSError:
        logging.warning('Ошибка открытия файла')


if __name__ == "__main__":
    try:
        os.makedirs('task_1')
        logging.info('Папка успешно создана')
        read_data_from_file()
    except OSError:
        logging.warning('Ошибка при создании папки')
