import csv
import os
import logging

logger = logging.getLogger()
logger.setLevel('INFO')


def write_data_to_files(data: list, path: str, dest_1: str = 'task_1/X.csv', dest_2: str = 'task_1/Y.csv') -> None:
    """
    Функция заисывает полученную строку в выбранный файл
    :param data: Файл, в который фунция записывает строку
    :param path: Путь к папке с файлами
    :param dest_1: Путь к файлу с датами
    :param dest_2: Путь к файлу со значениями
    :return: Функция не возвращает значение
    """
    try:
        with open(os.path.join(path, dest_1), 'a') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow([data[0]])
        with open(os.path.join(path, dest_2), 'a') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow([data[1]])
    except OSError as er:
        logging.warning(f'Ошибка открытия файла {er}')


def read_data_from_file(dest: str, source: str = "dataset.csv", last_date: str = "1992-07-01") -> None:
    """
    Функция считывает данные из файла
    :param dest: Путь к файлам, которые создаст программа
    :param source: Файл из которого происходит считывание данных
    :param last_date: Последняя дата в файле
    :return: Функция не возвращает никакое значения
    """
    try:
        with open(source, 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            for row in reader:
                write_data_to_files(row, dest)
                logging.info(f'Программа сейчас на дате: {row[0]}, '
                             f'последняя дата: {last_date}')
    except OSError as er:
        logging.warning(f'Ошибка открытия файла {er}')


if __name__ == "__main__":
    try:
        os.makedirs('task_1')
        logging.info('Папка успешно создана')
        read_data_from_file(os.getcwd())
    except OSError as er:
        logging.warning(f'Ошибка при создании папки {er}')