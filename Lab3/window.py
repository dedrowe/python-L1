import os
import re
import shutil
import sys
from datetime import datetime
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QFileDialog, QLineEdit, QLabel, \
    QVBoxLayout, QHBoxLayout
from task_1 import read_data_from_file
from task_2 import create_list_2
from task_3 import create_list_3
from task_4 import search_in_dataset, search_in_task_1, search_in_task_2_and_3


class Window(QMainWindow):
    """
    Класс реализует графический интерфейс для второй лабораторной
    """
    dataset_path: str = ''
    task_1_path: str = ''
    task_2_path: str = ''
    task_3_path: str = ''

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Искатель курса валют по дате 3000')
        self.resize(1280, 768)
        self.dataset_path = QFileDialog.getExistingDirectory(self, "Выберите путь к файлу с исходными данными")
        v = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        h4 = QHBoxLayout()
        h5 = QHBoxLayout()
        h6 = QHBoxLayout()
        self.dataset_path_label = QLabel(f'Путь к исходному файлу: {self.dataset_path}')
        self.task_1_path_label = QLabel('Путь к файлам разделенным по типам:')
        self.task_2_path_label = QLabel('Путь к файлам разделенным по годам:')
        self.task_3_path_label = QLabel('Путь к файлам разделенным по неделям:')
        date = QLabel('Введите нужную вам дату: ')
        self.value = QLabel()
        button_create_new_annotation = self.create_button(h1, 'Создать аннотацию', 200, 50)
        button_choose_dataset_path = self.create_button(h1, 'Выбрать путь', 200, 50)
        h1.addWidget(self.dataset_path_label)
        button_create_task_1_dataset = self.create_button(h2, 'Создать датасет из task_1', 200, 50)
        button_choose_task_1_path = self.create_button(h2, 'Выбрать путь', 200, 50)
        h2.addWidget(self.task_1_path_label)
        button_create_task_2_dataset = self.create_button(h3, 'Создать датасет из task_2', 200, 50)
        button_choose_task_2_path = self.create_button(h3, 'Выбрать путь', 200, 50)
        h3.addWidget(self.task_2_path_label)
        button_create_task_3_dataset = self.create_button(h4, 'Создать датасет из task_3', 200, 50)
        button_choose_task_3_path = self.create_button(h4, 'Выбрать путь', 200, 50)
        h4.addWidget(self.task_3_path_label)
        button_search_in_dataset = self.create_button(h6, 'Искать в исходном файле', 250, 50)
        button_search_in_task_1 = self.create_button(h6, 'Искать в разделенных по типу файлах', 250, 50)
        button_search_in_task_2 = self.create_button(h6, "Искать в разделенных по годам файлах", 250, 50)
        button_search_in_task_3 = self.create_button(h6, 'Искать в разделенных по неделям файлах', 250, 50)
        h6.addStretch(1)
        self.line = QLineEdit()
        h5.addWidget(date)
        h5.addWidget(self.line)
        h5.addWidget(self.value)
        h5.addStretch(1)
        v.addLayout(h1)
        v.addLayout(h2)
        v.addLayout(h3)
        v.addLayout(h4)
        v.addLayout(h5)
        v.addLayout(h6)
        v.addStretch(1)

        button_create_new_annotation.clicked.connect(self.copy_dataset)
        button_choose_dataset_path.clicked.connect(self.choose_path_for_dataset)
        button_create_task_1_dataset.clicked.connect(self.create_task_1_dataset)
        button_choose_task_1_path.clicked.connect(self.choose_path_for_task_1)
        button_create_task_2_dataset.clicked.connect(self.create_task_2_dataset)
        button_choose_task_2_path.clicked.connect(self.choose_path_for_task_2)
        button_create_task_3_dataset.clicked.connect(self.create_task_3_dataset)
        button_choose_task_3_path.clicked.connect(self.choose_path_for_task_3)
        button_search_in_dataset.clicked.connect(self.search_in_dataset)
        button_search_in_task_1.clicked.connect(self.search_in_task_1)
        button_search_in_task_2.clicked.connect(self.search_in_task_2)
        button_search_in_task_3.clicked.connect(self.search_in_task_3)

        container = QWidget()
        container.setLayout(v)
        self.setCentralWidget(container)
        self.show()

    @staticmethod
    def create_button(box, name: str, size_x: int, size_y: int) -> QPushButton:
        """
        Функция создает кнопку
        :param box: VBox для этой кнопки
        :param name: Имя кнопки
        :param size_x: Ширина кнопки
        :param size_y: Высота кнопки
        :return: Функция возвращает кнопку
        """
        button = QPushButton(name)
        button.setFixedSize(QSize(size_x, size_y))
        box.addWidget(button)
        return button

    def choose_path_for_dataset(self) -> None:
        """
        Функция позволяет пользователю ввести путь для изначального датасета
        :return: Функция не возвращает значение
        """
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            self.dataset_path = path
            self.dataset_path_label.setText(f'Путь к исходному файлу: {path}')
        else:
            self.dataset_path_label.setText('Ошибка')

    def choose_path_for_task_1(self) -> None:
        """
        Функция позволяет пользователю ввести путь для файлов для task_1
        :return: Функция не возвращает значение
        """
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            self.task_1_path = path
            self.task_1_path_label.setText(f'Путь к файлам разделенным по типам: {path}')
        else:
            self.task_1_path_label.setText('Ошибка')

    def choose_path_for_task_2(self) -> None:
        """
        Функция позволяет пользователю ввести путь для файлов для task_2
        :return: Функция не возвращает значение
        """
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            self.task_2_path = path
            self.task_2_path_label.setText(f'Путь к файлам разделенным по годам:: {path}')
        else:
            self.task_2_path_label.setText('Ошибка')

    def choose_path_for_task_3(self) -> None:
        """
        Функция позволяет пользователю ввести путь для файлов для task_3
        :return: Функция не возвращает значение
        """
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            self.task_3_path = path
            self.task_3_path_label.setText(f'Путь к файлам разделенным по неделям: {path}')
        else:
            self.task_3_path_label.setText('Ошибка')

    def copy_dataset(self) -> None:
        """
        Функция копирует начальный датасет
        :return: Функция не возвращает значение
        """
        if self.dataset_path:
            shutil.copyfile(os.path.join(self.dataset_path, 'dataset.csv'),
                            os.path.join(self.dataset_path, '../dataset.csv'))
            self.value.setText('Копирование выполнено успешно')

    def create_task_1_dataset(self) -> None:
        """
        Функция разбивает начальный файл на два: с датами и со значениями для этих дат
        :return: Функция не возвращает значение
        """
        if self.task_1_path:
            os.makedirs(os.path.join(self.task_1_path, 'task_1'))
            read_data_from_file(self.task_1_path)
            self.value.setText('Файлы созданы')
        else:
            self.value.setText('Ошибка при создании файлов')

    def create_task_2_dataset(self) -> None:
        """
        Функция разбивает изначальный файл по годам
        :return: Функция не возвращает значение
        """
        if self.task_2_path:
            path = os.path.join(self.task_2_path, 'task_2')
            os.makedirs(path)
            create_list_2(path)
            self.value.setText('Файлы созданы')
        else:
            self.value.setText('Ошибка при создании файлов')

    def create_task_3_dataset(self) -> None:
        """
        Функция разбивает изначальный файл по неделям
        :return: Функция не возвращает значение
        """
        if self.task_3_path:
            path = os.path.join(self.task_3_path, 'task_3')
            os.makedirs(path)
            create_list_3(path)
            self.value.setText('Файлы созданы')
        else:
            self.value.setText('Ошибка при создании файлов')

    def search_in_dataset(self) -> None:
        """
        Функция ищет значение для выбранной даты в начальном датасете
        :return: Функция не возвращает значение
        """
        temp = self.line.text()
        if re.match('\d{4}-\d\d-\d\d', temp):
            tmp = search_in_dataset(datetime.date(datetime.strptime(temp, "%Y-%m-%d")), self.dataset_path)
            if tmp is None:
                self.value.setText('Запись для такой даты не существует')
            else:
                self.value.setText(tmp[1])
        else:
            self.value.setText('Дата введена неверно')

    def search_in_task_1(self) -> None:
        """
        Функция ищет значение для выбранной даты в файлах из task_1
        :return: Функция не возвращает значение
        """
        temp = self.line.text()
        if re.match('\d{4}-\d\d-\d\d', temp):
            tmp = search_in_task_1(datetime.date(datetime.strptime(temp, "%Y-%m-%d")), self.task_1_path)
            if tmp is None:
                self.value.setText('Запись для такой даты не существует')
            else:
                self.value.setText(tmp)
        else:
            self.value.setText('Дата введена неверно')

    def search_in_task_2(self) -> None:
        """
        Функция ищет значение для выбранной даты в файлах из task_2
        :return: Функция не возвращает значение
        """
        temp = self.line.text()
        if re.match('\d{4}-\d\d-\d\d', temp):
            tmp = search_in_task_2_and_3(datetime.date(datetime.strptime(temp, "%Y-%m-%d")),
                                         os.path.join(self.task_2_path, 'task_2'))
            if tmp is None:
                self.value.setText('Запись для такой даты не существует')
            else:
                self.value.setText(tmp[1])
        else:
            self.value.setText('Дата введена неверно')

    def search_in_task_3(self) -> None:
        """
        Функция ищет значение для выбранной даты в файлах из task_3
        :return: Функция не возвращает значение
        """
        temp = self.line.text()
        if re.match('\d{4}-\d\d-\d\d', temp):
            tmp = search_in_task_2_and_3(datetime.date(datetime.strptime(temp, "%Y-%m-%d")),
                                         os.path.join(self.task_3_path, 'task_2'))
            if tmp is None:
                self.value.setText('Запись для такой даты не существует')
            else:
                self.value.setText(tmp[1])
        else:
            self.value.setText('Дата введена неверно')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    app.exec()
