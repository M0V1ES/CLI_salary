import argparse
import os

from create_report import create_file
from payout import create_report_payout
from validate_csv import read_csv


def csv_file(path: str) -> str:
    """Проверяет, что файл имеет расширение .csv"""
    if not path.lower().endswith(".csv"):
        raise argparse.ArgumentTypeError(f"Файлы должны иметь расширение .csv")
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"Файл '{path}' не существует")
    return path


def main():
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Создание отчетов",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Добавляем аргумент для файлов (nargs='+' означает минимум 1 файл)
    parser.add_argument(
        "files",
        metavar="FILE",
        type=csv_file,
        nargs="+",
        help="CSV файлы для обработки",
    )

    # Опциональные аргументы
    parser.add_argument(
        "--report",
        type=str,
        help="Название файла для сохранения отчета",
    )

    # Парсим аргументы
    args = parser.parse_args()
    try:
        csv = read_csv(args.files)
        data = create_report_payout(csv)
        create_file(args.report, data)
    except FileNotFoundError as e:
        print("Произошла ошибка при чтении файла", e)
    except Exception as e:
        print("Произошла непредвиденная ошибка.", e)


if __name__ == "__main__":
    main()
