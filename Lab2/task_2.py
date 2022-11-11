import csv
import os
import logging

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
                writer.writerow([i])
    except OSError:
        logging.warning('Ошибка открытия файла')


def create_list(source: str = "dataset.csv", last_row: str = "1992-07-01, 125.26") -> None:
    """
    Функция создает список данных из файла
    :param source: Файл, из которого программа считывает данные
    :param last_row: Последняя запись в файле
    :return: Фукнция не возвращает значение
    """
    try:
        with open(source, 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            rows = [next(reader)[0]]
            while rows[-1] != last_row:
                row = next(reader)[0]
                print(row)
                while rows[-1][:4] == row[:4] and row != last_row:
                    rows.append(row)
                    row = next(reader)[0]
                    logging.info(f'Программа сейчас на дате: {rows[-1].split(sep=", ")[0]}, '
                                 f'последняя дата: {last_row.split(sep=", ")[0]}')
                if row == last_row:
                    rows.append(row)
                path =\
                    f'task_2/{rows[-1][:4]}{rows[-1][5:7]}{rows[-1][8:10]}_{rows[0][:4]}{rows[0][5:7]}{rows[0][8:10]}'
                write_data_to_file(rows, path)
                rows = [row]
    except OSError:
        logging.warning('Ошибка открытия файла')


if __name__ == "__main__":
    try:
        os.makedirs('task_2')
        logging.info('Папка успешно создана')
        create_list()
    except OSError:
        logging.info('Ошибка при создании папки')
