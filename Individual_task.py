import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from datetime import datetime
import os

# список констант, используемых при вычислении хэша SHA-256
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


def generate_hash(message: bytearray) -> bytearray:
    """Возвращает хэш SHA-256 из переданного сообщения.
    Аргумент должен быть байтовым, массивом байтов или строковым объектом."""

    if isinstance(message, str):
        message = bytearray(message, 'ascii')
    elif isinstance(message, bytes):
        message = bytearray(message)
    elif not isinstance(message, bytearray):
        raise TypeError

    # Дополнение
    length = len(message) * 8  # len(message) - количество БАЙТОВ!!!
    message.append(0x80)
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0x00)

    message += length.to_bytes(8, 'big')  # дополнение до 8 байт или 64 бит

    assert (len(message) * 8) % 512 == 0, "Дополнение не выполнено правильно!"

    # Разбиение на блоки
    blocks = []  # содержит блоки по 512 бит сообщения
    for i in range(0, len(message), 64):  # 64 байта это 512 бит
        blocks.append(message[i:i + 64])

    # Установка начального значения хэша
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h5 = 0x9b05688c
    h4 = 0x510e527f
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    # Вычисление хэша SHA-256
    for message_block in blocks:
        # Подготовка расписания сообщения
        message_schedule = []
        for t in range(0, 64):
            if t <= 15:
                # добавляет t-е 32-битное слово блока,
                # начиная с левого слова
                # по 4 байта за раз
                message_schedule.append(bytes(message_block[t * 4:(t * 4) + 4]))
            else:
                term1 = _sigma1(int.from_bytes(message_schedule[t - 2], 'big'))
                term2 = int.from_bytes(message_schedule[t - 7], 'big')
                term3 = _sigma0(int.from_bytes(message_schedule[t - 15], 'big'))
                term4 = int.from_bytes(message_schedule[t - 16], 'big')

                # добавление 4-байтного объекта
                schedule = ((term1 + term2 + term3 + term4) % 2 ** 32).to_bytes(4, 'big')
                message_schedule.append(schedule)

        assert len(message_schedule) == 64

        # Инициализация рабочих переменных
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        # Итерация для t=0 до 63
        for t in range(64):
            t1 = ((h + _capsigma1(e) + _ch(e, f, g) + K[t] +
                   int.from_bytes(message_schedule[t], 'big')) % 2 ** 32)

            t2 = (_capsigma0(a) + _maj(a, b, c)) % 2 ** 32

            h = g
            g = f
            f = e
            e = (d + t1) % 2 ** 32
            d = c
            c = b
            b = a
            a = (t1 + t2) % 2 ** 32

        # Вычисление промежуточного значения хэша
        h0 = (h0 + a) % 2 ** 32
        h1 = (h1 + b) % 2 ** 32
        h2 = (h2 + c) % 2 ** 32
        h3 = (h3 + d) % 2 ** 32
        h4 = (h4 + e) % 2 ** 32
        h5 = (h5 + f) % 2 ** 32
        h6 = (h6 + g) % 2 ** 32
        h7 = (h7 + h) % 2 ** 32

    return ((h0).to_bytes(4, 'big') + (h1).to_bytes(4, 'big') +
            (h2).to_bytes(4, 'big') + (h3).to_bytes(4, 'big') +
            (h4).to_bytes(4, 'big') + (h5).to_bytes(4, 'big') +
            (h6).to_bytes(4, 'big') + (h7).to_bytes(4, 'big'))


def _sigma0(num: int):
    """Как определено в спецификации."""
    num = (_rotate_right(num, 7) ^
           _rotate_right(num, 18) ^
           (num >> 3))
    return num


def _sigma1(num: int):
    """Как определено в спецификации."""
    num = (_rotate_right(num, 17) ^
           _rotate_right(num, 19) ^
           (num >> 10))
    return num


def _capsigma0(num: int):
    """Как определено в спецификации."""
    num = (_rotate_right(num, 2) ^
           _rotate_right(num, 13) ^
           _rotate_right(num, 22))
    return num


def _capsigma1(num: int):
    """Как определено в спецификации."""
    num = (_rotate_right(num, 6) ^
           _rotate_right(num, 11) ^
           _rotate_right(num, 25))
    return num


def _ch(x: int, y: int, z: int):
    """Как определено в спецификации."""
    return (x & y) ^ (~x & z)


def _maj(x: int, y: int, z: int):
    """Как определено в спецификации."""
    return (x & y) ^ (x & z) ^ (y & z)


def _rotate_right(num: int, shift: int, size: int = 32):
    """Поворот целого числа вправо."""
    return (num >> shift) | (num << size - shift)


def calculate_file_hash(filename):
    """Вычисляет хэш-сумму файла с использованием SHA-256."""
    try:
        with open(filename, 'rb') as f:
            file_content = f.read()
            hash_result = generate_hash(file_content)
            return hash_result.hex()  # Возвращает хэш в виде шестнадцатеричной строки
    except IOError as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return None


def calculate_directory_hashes(directory_path):
    """Вычисляет хэш-суммы для всех файлов в указанной директории."""
    hashes = {}
    for root, _, files in os.walk(directory_path):
        for name in files:
            file_path = os.path.join(root, name)
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                hashes[file_path] = file_hash
    return hashes


def save_hashes(hashes, filename="hashes.txt"):
    """Сохраняет хэш-суммы в файл."""
    with open(filename, 'w') as file:
        for path, hash_sum in hashes.items():
            file.write(f"{path}:{hash_sum}\n")


def load_hashes(filename="hashes.txt"):
    """Загружает хэш-суммы из файла."""
    hashes = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                path, hash_sum = line.strip().rsplit(':', 1)
                hashes[path] = hash_sum
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    return hashes


def get_time():
    """Получение времени."""
    now = datetime.now()
    formatted_datetime = now.strftime("%H:%M:%S %d.%m.%Y")
    return formatted_datetime


def verify_integrity_ui(directory_path, saved_hashes, output_widget, gui):
    """Проверка целостности файлов с выводом результатов в GUI."""
    current_hashes = calculate_directory_hashes(directory_path)
    integrity_broken = False
    for path, saved_hash in saved_hashes.items():
        if path in current_hashes:
            if current_hashes[path] != saved_hash:
                output_widget.append(f"Целостность нарушена: {path} - {get_time()}\n")
                integrity_broken = True
                gui.fileChangedHandler()
            else:
                output_widget.append(f"Целостность подтверждена: {path} - {get_time()}\n")
                gui.error_flag = False
        else:
            output_widget.append(f"Файл не найден: {path} - {get_time()}\n")
            integrity_broken = True

    for path in current_hashes:
        if path not in saved_hashes:
            output_widget.append(f"Новый файл: {path} - {get_time()}\n")
            integrity_broken = True

    if not integrity_broken:
        output_widget.append(f"Все файлы прошли проверку целостности - {get_time()}\n")
        gui.error_flag = False


class FileIntegrityChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selectedDirectory = None
        self.error_flag = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.autoCheckIntegrity)

    def initUI(self):
        self.setWindowTitle('Проверка целостности файлов')
        self.setWindowIcon(QIcon())
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.directoryLabel = QLabel('Выберите директорию для мониторинга')
        layout.addWidget(self.directoryLabel)

        self.browseButton = QPushButton('Выбрать директорию')
        self.browseButton.clicked.connect(self.openFileDialog)
        layout.addWidget(self.browseButton)

        self.checkButton = QPushButton('Проверить целостность')
        self.checkButton.clicked.connect(self.checkIntegrity)
        layout.addWidget(self.checkButton)

        self.resultText = QTextEdit()
        self.resultText.setReadOnly(True)
        layout.addWidget(self.resultText)

        self.setLayout(layout)

    def openFileDialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Выбрать директорию")
        if directory:
            self.directoryLabel.setText(f"Текущая директория - {directory}")
            self.selectedDirectory = directory
            hashes_file_path = os.path.join('hashes.txt')
            # Удаление файла hashes.txt, если он существует
            if os.path.exists(hashes_file_path):
                os.remove(hashes_file_path)

    def checkIntegrity(self):
        # self.resultText.clear()
        if self.selectedDirectory:
            # Путь к файлу hashes.txt в текущей директории
            hashes_file_path = os.path.join('hashes.txt')

            if not os.path.exists(hashes_file_path):
                # Создание хешей для текущей директории и сохранение их в файл
                hashes = calculate_directory_hashes(self.selectedDirectory)
                save_hashes(hashes, hashes_file_path)
                self.resultText.clear()
                self.resultText.append(f"Новый список хешей создан - {get_time()}\n")
                self.timer.start(60000)
                self.error_flag = False
            else:
                # Файл hashes.txt найден, продолжаем проверку целостности
                loaded_hashes = load_hashes(hashes_file_path)
                verify_integrity_ui(self.selectedDirectory, loaded_hashes, self.resultText, self)
        else:
            self.resultText.clear()
            self.resultText.append("Директория не выбрана.")

    def autoCheckIntegrity(self):
        if self.selectedDirectory:
            # self.resultText.clear()
            self.checkIntegrity()

    def fileChangedHandler(self):
        if not self.error_flag:
            QMessageBox.information(self, "Уведомление", f"В директории {self.selectedDirectory} произошли изменения!")
            self.error_flag = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileIntegrityChecker()
    ex.show()
    sys.exit(app.exec_())
