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


def create_list(source: str = 'dataset.csv', last_date: str = "1992-07-01"):
    with open(source, 'r') as dataset:
        reader = csv.reader(dataset, dialect='unix')
        rows = [next(reader)]
        for row in reader:
            temp1 = rows[-1][0].split(sep='-')
            logging.info(f'Программа сейчас на дате: {row[0]}, '
                         f'последняя дата: {last_date}')
            temp2 = row[0].split(sep='-')
            if datetime.date(int(temp1[0]), int(temp1[1]), int(temp1[2])).isocalendar()[1] == \
                    datetime.date(int(temp2[0]), int(temp2[1]), int(temp2[2])).isocalendar()[1]:
                rows.append(row)
            else:
                path = f'task_3/{rows[-1][0][:4]}{rows[-1][0][5:7]}{rows[-1][0][8:10]}' \
                       f'_{rows[0][0][:4]}{rows[0][0][5:7]}{rows[0][0][8:10]}'
                write_data_to_file(rows, path)
                rows = [row]
        path = f'task_3/{rows[-1][0][:4]}{rows[-1][0][5:7]}{rows[-1][0][8:10]}' \
               f'_{rows[0][0][:4]}{rows[0][0][5:7]}{rows[0][0][8:10]}'
        write_data_to_file(rows, path)


if __name__ == "__main__":
    try:
        os.makedirs('task_3')
        logging.info('Папка успешно создана')
    except OSError:
        logging.info('Ошибка при создании папки')
    create_list()
