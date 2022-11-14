import csv
import datetime
import logging
import os


logger = logging.getLogger()
logger.setLevel('INFO')


def read_dataset(source: str = 'dataset.csv') -> list:
    """
    Функция считывает файл и возвращает его как список
    :param source: Файл из которого происходит считывание
    :return: Функция возвращает список
    """
    with open(source, 'r') as dataset:
        reader = csv.reader(dataset, dialect='unix')
        rows = []
        for row in reader:
            rows.append(row)
        return rows


def func_next() -> tuple:
    """
    Функция, которая при первом вызове возвращает данные для самой ранней возможной даты
    (возвращается кортеж (дата, данные)), а при каждом следующем вызове данные для следующей по порядку даты  в файле
    Название изменено из-за конфликта с next(reader)
    :return: Функция возвращает кортеж (дата, данные)
    """
    data_list = read_dataset()
    func_next.count -= 1
    return data_list[func_next.count][0], data_list[func_next.count][1]


func_next.count = 0


def search_in_dataset(date: datetime.date, source: str = "dataset.csv", last_date: str = "1992-07-01") -> list:
    """
    Функция прнимает дату и ищет данные для нее а изначальном файле
    :param date: Дата по которой происходит поиск
    :param source: Изначальный файл
    :param last_date: Последняя запись в файле
    :return: Функция возвращает список вида (дата, значение)
    """
    try:
        with open(source, 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            for row in reader:
                logging.info(f'Программа сейчас на дате: {row[0]}, '
                             f'последняя дата: {last_date}')
                temp = row[0].split(sep='-')
                temp_date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
                if temp_date >= date:
                    if row[0] == str(date):
                        return row
                if row[0] == str(date):
                    return row
            return [None]
    except OSError:
        logging.error("Ошибка открытия файла")


def search_in_task_1(date: datetime.date, source_1: str = "task_1/X.csv", source_2: str = "task_1/Y.csv",
                     last_date: str = "1992-07-01") -> list:
    """
    Функция принимает дату и ищет данные для нее в файлах полученных в первом задании
    :param date: Дата по которой происходит поиск
    :param source_1: Путь к файлу с датами
    :param source_2: Путь к файлу со значениями
    :param last_date: Последняя дата в файле с датами
    :return: Функция возвращает список вида (дата, значение)
    """
    try:
        with open(source_1, 'r') as date_list:
            with open(source_2, 'r') as value_list:
                reader_1 = csv.reader(date_list, dialect='unix')
                reader_2 = csv.reader(value_list, dialect='unix')
                for row_1 in reader_1:
                    logging.info(f'Программа сейчас на дате: {row_1[0]}, '
                                 f'последняя дата: {last_date}')
                    row_2 = next(reader_2)
                    temp = row_1[0].split(sep='-')
                    temp_date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
                    if temp_date >= date:
                        if row_1[0] == str(date):
                            return [row_1[0], row_2[0]]
            return [None]
    except OSError:
        logging.error("Ошибка открытия файла")


def search_in_task_2_and_3(date: datetime.date, source: str) -> list:
    """
    Функция перебирает файлы в полученной папке и выводит значение для введенной даты
    :param date: Дата по которой происходит поиск
    :param source: Папка с файлами в которых происходит поиск
    :return: Функция возвращает список вида (датаб значение)
    """
    for filename in os.listdir(source):
        with open(os.path.join(source, filename), 'r') as dataset:
            reader = csv.reader(dataset, dialect='unix')
            for row in reader:
                if row[0] == str(date):
                    return row
    return [None]


if __name__ == "__main__":
    user_input = str(input()).split(sep='-')
    print("Выберите тип входных файлов:")
    print("1 - один файл со всеми данными")
    print("2 - два файла (в одном даты, в другом значения для них")
    print("3 - файлы по годам")
    print("4 - файлы по неделям")
    a = datetime.date(int(user_input[0]), int(user_input[1]), int(user_input[2]))
    print(func_next())
    print(func_next())
    flag = int(input())
    match flag:
        case 1:
            print(search_in_dataset(a))
        case 2:
            print(search_in_task_1(a))
        case 3:
            print(search_in_task_2_and_3(a, 'task_2'))
        case 4:
            print(search_in_task_2_and_3(a, 'task_3'))
