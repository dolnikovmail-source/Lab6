
import os
import subprocess
import sys


def get_build_command():
    """
    Формирует список аргументов для вызова PyInstaller:
    - --onefile: сборка в один исполняемый файл
    - --windowed (или --noconsole): скрытие консольного окна для GUI
    - --name: имя результирующего .exe файла
    - --clean: очистка кэша сборки перед стартом
    """
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=PhotoEditor",
        "--clean",
        "photo_editor.py",
    ]
    return cmd


def run_build():
    """Запускает процесс сборки через утилиту PyInstaller."""
    cmd = get_build_command()
    print("=" * 60)
    print(f"Запуск сборки: {' '.join(cmd)}")
    print("=" * 60)

    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError("Ошибка при выполнении сборки PyInstaller!")
    print("\nПроцесс упаковки PyInstaller успешно завершён!")


def test_executable():
    """Проверяет наличие и размер собранного исполняемого файла."""
    exe_path = os.path.join("dist", "PhotoEditor.exe")

    print("=" * 60)
    print("Проверка результатов сборки:")
    if os.path.exists(exe_path):
        size_bytes = os.path.getsize(exe_path)
        size_mb = size_bytes / (1024 * 1024)
        print(f"[УСПЕХ] Файл найден: {exe_path}")
        print(f"[ИНФО] Размер дистрибутива: {size_mb:.2f} МБ ({size_bytes} байт)")
        print("Дистрибутив готов к автономному запуску без установленного Python.")
    else:
        print(f"[ОШИБКА] Исполняемый файл не найден по пути: {exe_path}")
    print("=" * 60)


if __name__ == "__main__":
    print("Начинаю сборку дистрибутива приложения...\n")
    try:
        run_build()
        test_executable()
        print("\nСборка полностью завершена!")
    except Exception as err:
        print(f"\nОшибка сборки: {err}", file=sys.stderr)
        sys.exit(1)