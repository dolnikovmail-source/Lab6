
import sys
import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PhotoEditor(QMainWindow):
    """Главное окно приложения 'Фоторедактор'."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фоторедактор — Вариант 1")
        self.resize(750, 550)

        # Хранилища для оригинального и обработанного изображения (массивы OpenCV)
        self.original_image = None
        self.processed_image = None

        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Область для отображения изображения
        self.image_label = QLabel("Загрузите изображение для начала работы")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #888; background-color: #222; color: #aaa;")
        main_layout.addWidget(self.image_label, stretch=1)

        # Информационная строка состояния
        self.status_label = QLabel("Готово к работе")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Панель кнопок управления
        buttons_layout = QHBoxLayout()

        self.btn_load = QPushButton("Загрузить")
        self.btn_gray = QPushButton("Оттенки серого")
        self.btn_reset = QPushButton("Оригинал")
        self.btn_save = QPushButton("Сохранить")

        # Привязка сигналов к слотам
        self.btn_load.clicked.connect(self.load_image)
        self.btn_gray.clicked.connect(self.apply_grayscale)
        self.btn_reset.clicked.connect(self.reset_image)
        self.btn_save.clicked.connect(self.save_image)

        # Добавление кнопок в горизонтальный ряд
        buttons_layout.addWidget(self.btn_load)
        buttons_layout.addWidget(self.btn_gray)
        buttons_layout.addWidget(self.btn_reset)
        buttons_layout.addWidget(self.btn_save)

        main_layout.addLayout(buttons_layout)
        central_widget.setLayout(main_layout)

    def display_image(self, cv_img):
        """Преобразует изображение OpenCV (BGR) в QPixmap и выводит на экран."""
        if cv_img is None:
            return

        # Конвертация цветового пространства из BGR в RGB для корректного отображения
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width

        # Создание объекта QImage
        q_img = QImage(
            rgb_image.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        # Масштабирование под размер области просмотра с сохранением пропорций
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            self.image_label.width() - 20,
            self.image_label.height() - 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

    def load_image(self):
        """Загрузка изображения через диалоговое окно."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.jpg *.jpeg *.png *.bmp)"
        )

        if not file_path:
            return

        img = cv2.imread(file_path)
        if img is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить выбранное изображение.")
            return

        self.original_image = img
        self.processed_image = img.copy()
        self.display_image(self.processed_image)
        self.status_label.setText(f"Загружен файл: {file_path}")

    def apply_grayscale(self):
        """Преобразование изображения в оттенки серого."""
        if self.original_image is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала загрузите изображение!")
            return

        # Преобразование в оттенки серого
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        # Обратное преобразование в 3 канала (BGR) для совместимости с QImage RGB888
        self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        self.display_image(self.processed_image)
        self.status_label.setText("Применён фильтр: Оттенки серого")

    def reset_image(self):
        """Сброс к исходному цветному изображению."""
        if self.original_image is None:
            return

        self.processed_image = self.original_image.copy()
        self.display_image(self.processed_image)
        self.status_label.setText("Возвращено исходное изображение")

    def save_image(self):
        """Сохранение обработанного изображения на диск."""
        if self.processed_image is None:
            QMessageBox.warning(self, "Предупреждение", "Нет изображения для сохранения!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить изображение как...",
            "output.jpg",
            "JPEG (*.jpg);;PNG (*.png);;Все файлы (*.*)"
        )

        if file_path:
            success = cv2.imwrite(file_path, self.processed_image)
            if success:
                self.status_label.setText(f"Файл успешно сохранён: {file_path}")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить файл.")


def main():
    """Точка запуска приложения."""
    app = QApplication(sys.argv)
    window = PhotoEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()