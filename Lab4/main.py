import pandas as pd
from functools import partial
import math
import matplotlib.pyplot as plt
import logging
import numpy as np


logger = logging.getLogger()
logger.setLevel('INFO')


def create_dataframe(source: str = 'dataset.csv') -> pd.DataFrame:
    """
    Функция ситывает данные из файла и превращает их в датафрейм
    :param source: Путь к файлу
    :return: Функция возвращает датафрейм
    """
    frame = pd.read_csv(source, sep=",", names=['date', 'value'])
    frame.date = pd.to_datetime(frame.date, format='%Y-%m-%d')
    delete_invalid_rows(frame)
    add_median_and_average_value_columns(frame)
    return frame


def delete_invalid_rows(frame: pd.DataFrame) -> None:
    """
    Функция удаляет из датафрейма строки с невалидными значениями
    :param frame: Датафрейм из которого происходит удаление
    :return: Функция не возвращает значение
    """
    i = 0
    while i < frame.shape[0]:
        temp = frame.iloc[i]['value']
        if temp is None or temp <= 0 or math.isnan(temp):
            frame.drop(index=i, inplace=True)
            i += 1
        i += 1


def add_median_and_average_value_columns(frame: pd.DataFrame) -> None:
    """
    Функция добавляет в датафрейм столбцы со средним значением и медианой
    :param frame: Датафрейм в который происходит добавление
    :return: Функция не возвращает значение
    """
    frame['median'] = frame['value'] - frame['value'].median()
    frame['average'] = frame['value'] - frame['value'].mean()


def filter_by_deviation(frame: pd.DataFrame, deviation: float) -> pd.DataFrame:
    """
    Функция фильтрует датафрейм по заданному отклонению от среднего значения
    :param frame: Датафрейм, который функция фильтрует
    :param deviation: Отклонение, относительно которого происходит фильтрация
    :return: Функция возвращает отфильтрованный датасет
    """
    return frame[frame.average >= deviation]


def filter_by_date(frame: pd.DataFrame, min_date: pd.Timestamp, max_date: pd.Timestamp) -> pd.DataFrame:
    """
    Функция фильтрует датафрейм по заданным датам
    :param frame: Датафрейм, который функция сортирует
    :param min_date: Минимальная дата для сртировки
    :param max_date: Максимальная дата для ортировки
    :return: Функция не возвращает значение
    """
    return frame[(min_date <= frame.date) & (frame.date <= max_date)]


def group_by_month(frame: pd.DataFrame) -> pd.DataFrame:
    """
    функция группирует датафрейм по месяцам
    :param frame: Датафрейм, который функция группирует
    :return: Функция возвращает сгруппированный датафрейм
    """
    return frame.groupby(pd.Grouper(key='date', freq='M')).mean()


def draw_value_chart(frame: pd.DataFrame, x_value: str = "date", y_value: str = "value", name: str = 'Value') -> None:
    """
    Функция рисует график в выбранных осях на основе датафрейма
    :param frame: Датафрейм на основе которого рисуется график
    :param x_value: Значение, которое будет откладываться по оси x
    :param y_value: Значение, которое будет откладываться по оси y
    :param name: Название графика
    :return: Функция не возвращает значение
    """
    temp = plt.subplot()
    temp.plot(frame[x_value], frame[y_value])
    temp.set_yscale('log')
    plt.title(name)
    plt.show()


def draw_value_chart_for_one_month(frame: pd.DataFrame, date: pd.Timestamp) -> None:
    """
    Функция принимает на вход датафрейм и дату, а затем для месяца с этой датой
    последовательно вызывает отрисовку графиков курса валюты, медианы и среднего значения
    :param frame: Датафрейм по которому будут рисоваться графики
    :param date: Дата, по которой определяется месяц
    :return: Функция не возвращает значение
    """
    date_1 = pd.Timestamp(date.year, date.month, 1)
    date_2 = pd.Timestamp(date.year, date.month, date_1.days_in_month)
    temp_frame = filter_by_date(frame, date_1, date_2)
    draw_value_chart(temp_frame)
    draw_value_chart(temp_frame, "date", "median", "Median")
    draw_value_chart(temp_frame, "date", "average", "Average")


if __name__ == "__main__":
    a = create_dataframe()
    while True:
        print("Чтобы заново считать датафрейм из файла нажмите 1")
        print("Чтобы отфильтровать датафрейм по отклонению от среднего значения нажмите 2")
        print("Чтобы отфильтровать датафрейм по датам нажмите 3")
        print("Чтобы сгруппировать датафрейм по месяцам нажмите 4")
        print("Чтобы нарисовать график значений нажмите 5")
        print("Чтобы нарисовать график за выбранный месяц нажмите 6")
        print("Чтобы выйти нажмите 7")
        flag = int(input())
        match flag:
            case 1:
                a = create_dataframe()
            case 2:
                print("Введите отклонение: ")
                dev = float(input())
                a = filter_by_deviation(a, dev).to_csv("filtered_by_deviation.csv")
            case 3:
                print("Введите начальную дату: ")
                date_1 = pd.Timestamp(input())
                print("Введите конечную дату: ")
                date_2 = pd.Timestamp(input())
                a = filter_by_date(a, date_1, date_2)
            case 4:
                a = group_by_month(a).to_csv("grouped_by_month.csv")
            case 5:
                draw_value_chart(a)
            case 6:
                print("Введите дату: ")
                date = pd.Timestamp(input())
                draw_value_chart_for_one_month(a, date)
            case 7:
                break
