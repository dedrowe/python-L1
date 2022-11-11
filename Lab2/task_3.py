import csv
import logging
import os
import datetime


logger = logging.getLogger()
logger.setLevel('INFO')


def write_data_to_file(data: list, destination: str) -> None:
    try:
        with open(destination, 'w') as f:
            for i in data:
                writer = csv.writer(f, dialect='unix')
                writer.writerow([i])
    except OSError:
        logging.warning('Ошибка открытия файла')


def parse_data(data: str) -> list:
    date = data.split(sep='-')
    return date


def create_list(source: str = 'dataset.csv', last_row: str = "1992-07-01, 125.26"):
    with open(source, 'r') as dataset:
        reader = csv.reader(dataset, dialect='unix')
        row = next(reader)[0]
        rows = [row]
        while row != last_row:
            temp1 = parse_data(row.split(sep=', ')[0])
            logging.info(f'Программа сейчас на дате: {row.split(sep=", ")[0]}, '
                         f'последняя дата: {last_row.split(sep=", ")[0]}')
            row = next(reader)[0]
            temp2 = parse_data(row.split(sep=', ')[0])
            if datetime.date(int(temp1[0]), int(temp1[1]), int(temp1[2])).isocalendar()[1] == \
                    datetime.date(int(temp2[0]), int(temp2[1]), int(temp2[2])).isocalendar()[1]:
                rows.append(row)
            else:
                path =\
                    f'task_3/{rows[-1][:4]}{rows[-1][5:7]}{rows[-1][8:10]}_{rows[0][:4]}{rows[0][5:7]}{rows[0][8:10]}'
                write_data_to_file(rows, path)
                rows = [row]
        path = f'task_3/{rows[-1][:4]}{rows[-1][5:7]}{rows[-1][8:10]}_{rows[0][:4]}{rows[0][5:7]}{rows[0][8:10]}'
        write_data_to_file(rows, path)


if __name__ == "__main__":
    try:
        os.makedirs('task_3')
        logging.info('Папка успешно создана')
    except OSError:
        logging.info('Ошибка при создании папки')
    create_list()
