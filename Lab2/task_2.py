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
                writer.writerow(i)
    except OSError:
        logging.warning('Ошибка открытия файла')


def create_list(source: str = "dataset.csv", last_date: str = "1992-07-01") -> None:
    """
    Функция создает список данных из файла
    :param source: Файл, из которого программа считывает данные
    :param last_date: Последняя дата в файле
    :return: Фукнция не возвращает значение
    """
    try:
        with open(source, 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            rows = [next(reader)]
            for row in reader:
                if rows[-1][0][:4] != row[0][:4]:
                    path =\
                        f'task_2/{rows[-1][0][:4]}{rows[-1][0][5:7]}{rows[-1][0][8:10]}_' \
                        f'{rows[0][0][:4]}{rows[0][0][5:7]}{rows[0][0][8:10]}'
                    write_data_to_file(rows, path)
                    rows = [row]
                else:
                    rows.append(row)
                logging.info(f'Программа сейчас на дате: {rows[-1][0]}, '
                             f'последняя дата: {last_date}')
            path = \
                f'task_2/{rows[-1][0][:4]}{rows[-1][0][5:7]}{rows[-1][0][8:10]}_' \
                f'{rows[0][0][:4]}{rows[0][0][5:7]}{rows[0][0][8:10]}'
            write_data_to_file(rows, path)
    except OSError:
        logging.warning('Ошибка открытия файла')


if __name__ == "__main__":
    try:
        os.makedirs('task_2')
        logging.info('Папка успешно создана')
        create_list()
    except OSError:
        logging.info('Ошибка при создании папки')
