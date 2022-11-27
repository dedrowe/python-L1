import os
import re
import shutil
import sys
from datetime import datetime
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QFileDialog, QLineEdit, QLabel, QVBoxLayout
from task_1 import read_data_from_file
from task_2 import create_list_2
from task_3 import create_list_3
from task_4 import search_in_dataset


class Window(QMainWindow):
    dataset_path: str

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lab_3')
        self.resize(1280, 768)
        v = QVBoxLayout()
        self.value = QLabel()
        self.dataset_path = QFileDialog.getExistingDirectory(self, "Выберите путь к файлу с исходными данными")
        v.addStretch(1)
        button_create_new_annotation = self.create_button(v, 'Создать аннотацию', 220, 50)
        button_create_task_1_dataset = self.create_button(v, 'Создать датасет из task_1', 220, 50)
        button_create_task_2_dataset = self.create_button(v, 'Создать датасет из task_2', 220, 50)
        button_create_task_3_dataset = self.create_button(v, 'Создать датасет из task_3', 220, 50)
        button_search_in_dataset = self.create_button(v, 'Получить данные', 220, 50)
        self.line = QLineEdit()
        v.addWidget(self.line)
        v.addWidget(self.value)

        button_create_new_annotation.clicked.connect(self.copy_dataset)
        button_create_task_1_dataset.clicked.connect(self.create_task_1_dataset)
        button_create_task_2_dataset.clicked.connect(self.create_task_2_dataset)
        button_create_task_3_dataset.clicked.connect(self.create_task_3_dataset)
        button_search_in_dataset.clicked.connect(self.search)

        container = QWidget()
        container.setLayout(v)
        container.setFixedSize(230, 325)
        self.setCentralWidget(container)
        self.show()

    @staticmethod
    def create_button(box, name: str, size_x: int, size_y: int) -> QPushButton:
        button = QPushButton(name)
        button.setFixedSize(QSize(size_x, size_y))
        box.addWidget(button)
        return button

    def copy_dataset(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            shutil.copyfile(os.path.join(self.dataset_path, 'dataset.csv'), os.path.join(path, 'dataset.csv'))
            self.value.setText('Копирование выполнено успешно')

    def create_task_1_dataset(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            os.makedirs(os.path.join(path, 'task_1'))
            read_data_from_file(path)
            self.value.setText('Файлы созданы')
        else:
            self.value.setText('Ошибка при создании файлов')

    def create_task_2_dataset(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            path = os.path.join(path, 'task_2')
            os.makedirs(path)
            create_list_2(path)
            self.value.setText('Файлы созданы')
        else:
            self.value.setText('Ошибка при создании файлов')

    def create_task_3_dataset(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Выберите путь к новому файлу")
        if path:
            path = os.path.join(path, 'task_3')
            os.makedirs(path)
            create_list_3(path)
            self.value.setText('Файлы созданы')
        else:
            self.value.setText('Ошибка при создании файлов')

    def search(self) -> None:
        temp = self.line.text()
        if re.match('\d{4}-\d\d-\d\d', temp):
            tmp = search_in_dataset(datetime.date(datetime.strptime(temp, "%Y-%m-%d")))
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
