import argparse
import unittest
import pytest

from main import csv_file
from payout import create_report_payout
from validate_csv import read_csv, remove_columns


def test_read_csv(tmp_path):
    csv_data = """id,email,name,department,hours_worked,hourly_rate
    1,alice@example.com,Alice Johnson,Marketing,160,50
    2,bob@example.com,Bob Smith,Design,150,40
    3,carol@example.com,Carol Williams,Design,170,60"""
    expected = [
        ("Marketing", "Alice Johnson", "160", "50"),
        ("Design", "Bob Smith", "150", "40"),
        ("Design", "Carol Williams", "170", "60"),
    ]
    csv = tmp_path / "test.csv"
    csv.write_text(csv_data)
    result = read_csv([str(csv)])
    assert result == expected


def test_empty_read_csv(tmp_path):
    csv_data = """id,email,name,department,hours_worked,hourly_rate"""
    expected = []
    csv = tmp_path / "test.csv"
    csv.write_text(csv_data)
    result = read_csv([str(csv)])
    assert result == expected


def test_several_read_csv(tmp_path):
    csv_data = """id,email,name,department,hours_worked,hourly_rate
    1,alice@example.com,Alice Johnson,Marketing,160,50
    2,bob@example.com,Bob Smith,Design,150,40
    3,carol@example.com,Carol Williams,Design,170,60"""
    csv_data1 = """id,email,name,department,hours_worked,hourly_rate
    1,alice@example.com,Alice,Marketing,160,50
    2,bob@example.com,Bob,Design,150,40
    3,carol@example.com,Carol,Design,170,60"""
    csv_data2 = """id,email,name,department,hours_worked,hourly_rate
    1,alice@example.com,Johnson,Marketing,160,50
    2,bob@example.com,Smith,Design,150,40
    3,carol@example.com,Williams,Design,170,60"""
    expected = [
        ("Marketing", "Alice Johnson", "160", "50"),
        ("Design", "Bob Smith", "150", "40"),
        ("Design", "Carol Williams", "170", "60"),
        ("Marketing", "Alice", "160", "50"),
        ("Design", "Bob", "150", "40"),
        ("Design", "Carol", "170", "60"),
        ("Marketing", "Johnson", "160", "50"),
        ("Design", "Smith", "150", "40"),
        ("Design", "Williams", "170", "60"),
    ]
    csv = tmp_path / "test.csv"
    csv1 = tmp_path / "test1.csv"
    csv2 = tmp_path / "test2.csv"
    csv.write_text(csv_data)
    csv1.write_text(csv_data1)
    csv2.write_text(csv_data2)
    result = read_csv([str(csv), str(csv1), str(csv2)])
    assert result == expected


def test_changed_name_column_read_csv(tmp_path):
    csv_data = """id,email,name,department,hours_worked,rate
    1,alice@example.com,Alice Johnson,Marketing,160,50
    2,bob@example.com,Bob Smith,Design,150,40
    3,carol@example.com,Carol Williams,Design,170,60"""
    csv_data1 = """id,email,name,department,hours_worked,hourly_rate
    1,alice@example.com,Alice,Marketing,160,50
    2,bob@example.com,Bob,Design,150,40
    3,carol@example.com,Carol,Design,170,60"""
    csv_data2 = """id,email,name,department,hours_worked,salary
    1,alice@example.com,Johnson,Marketing,160,50
    2,bob@example.com,Smith,Design,150,40
    3,carol@example.com,Williams,Design,170,60"""
    csv_data3 = """id,email,name,department,salary,hours_worked
        1,alice@example.com,Ivanov,Marketing,50,160
        2,bob@example.com,Smirnov,Design,40,150
        3,carol@example.com,Popov,Design,60,170"""
    expected = [
        ("Marketing", "Alice Johnson", "160", "50"),
        ("Design", "Bob Smith", "150", "40"),
        ("Design", "Carol Williams", "170", "60"),
        ("Marketing", "Alice", "160", "50"),
        ("Design", "Bob", "150", "40"),
        ("Design", "Carol", "170", "60"),
        ("Marketing", "Johnson", "160", "50"),
        ("Design", "Smith", "150", "40"),
        ("Design", "Williams", "170", "60"),
        ("Marketing", "Ivanov", "160", "50"),
        ("Design", "Smirnov", "150", "40"),
        ("Design", "Popov", "170", "60"),
    ]
    csv = tmp_path / "test.csv"
    csv1 = tmp_path / "test1.csv"
    csv2 = tmp_path / "test2.csv"
    csv3 = tmp_path / "test3.csv"
    csv.write_text(csv_data)
    csv1.write_text(csv_data1)
    csv2.write_text(csv_data2)
    csv3.write_text(csv_data3)
    result = read_csv([str(csv), str(csv1), str(csv2), str(csv3)])
    assert result == expected


def test_remove_columns():
    csv_data = [
        ("id", "name", "department", "hours_worked", "rate", "age"),
        ("1", "Alice Johnson", "Marketing", "160", "50", "45"),
        ("2", "Bob Smith", "Design", "150", "40", "55"),
        ("3", "Carol Williams", "Design", "170", "60", "19"),
    ]

    expected = [
        ("name", "department", "hours_worked", "rate"),
        ("Alice Johnson", "Marketing", "160", "50"),
        ("Bob Smith", "Design", "150", "40"),
        ("Carol Williams", "Design", "170", "60"),
    ]
    result = remove_columns(csv_data, ["id", "age"])

    assert result == expected


def test_csv_file(tmp_path):
    csv = tmp_path / "test.csv"
    csv.write_text("123")
    result = csv_file(str(csv))
    expected = str(csv)
    assert result == expected


def test_csv_file_not_exists(tmp_path):
    non_existent_file = tmp_path / "nonexistent.csv"
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        csv_file(str(non_existent_file))
    assert f"Файл '{non_existent_file}' не существует" in str(exc_info.value)


def test_csv_file_invalid_extension(tmp_path):
    txt_file = tmp_path / "file.txt"
    txt_file.write_text("test")
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        csv_file(str(txt_file))
    assert "Файлы должны иметь расширение .csv" in str(exc_info.value)


def test_single_employee():
    csv_data = [["IT", "John Doe", "160", "50"]]
    expected_output = (
        "      name            hours      rate    payout\n"
        "IT\n"
        "-----John Doe         160        50     $8000\n"
        "                      160               $8000\n"
    )
    result = create_report_payout(csv_data)
    assert result == expected_output


def test_duo_employee():
    csv_data = [["IT", "John Doe", "160", "50"], ["IT", "Ivan Ivanov", "30", "20"]]
    expected_output = (
        "      name            hours      rate    payout\n"
        "IT\n"
        "-----John Doe         160        50     $8000\n"
        "-----Ivan Ivanov       30        20      $600\n"
        "                      190               $8600\n"
    )
    result = create_report_payout(csv_data)
    assert result == expected_output


def test_multiple_departments():
    csv_data = [["IT", "John", "160", "50"], ["HR", "Anna", "120", "45"]]

    expected_output = (
        "      name            hours      rate    payout\n"
        "IT\n"
        "-----John             160        50     $8000\n"
        "                      160               $8000\n"
        "HR\n"
        "-----Anna             120        45     $5400\n"
        "                      120               $5400\n"
    )
    result = create_report_payout(csv_data)
    assert result == expected_output


def test_zero_hours():
    csv_data = [["IT", "John", "0", "50"]]
    expected_output = (
        "      name            hours      rate    payout\n"
        "IT\n"
        "-----John               0        50        $0\n"
        "                        0                  $0\n"
    )
    result = create_report_payout(csv_data)
    assert result == expected_output


def test_empty_input():
    csv_data = []
    expected_output = "      name            hours      rate    payout\n"
    result = create_report_payout(csv_data)
    assert result == expected_output


if __name__ == "__main__":
    unittest.main()
