def remove_columns(
    data: list,
    columns_to_remove: list,
) -> list:  # Функция для удаления колонок id и email
    # Определяем индексы колонок, которые нужно удалить
    header = data[0]
    remove_indices = []
    for i, col in enumerate(header):
        if col in columns_to_remove:
            remove_indices.append(i)

    new_data = []
    for row in data:
        filtered_row = tuple(
            item for i, item in enumerate(row) if i not in remove_indices
        )  # находим отфильтрованные колонки, без учета ненужных
        # создаем генератор пар(индекс, значение), если индекс переменной не находится в списке колонок на удаление, то сохраняем название переменной
        new_data.append(filtered_row)

    return new_data


def standardize_structure(
    data: list,
) -> list:  # Функция для стандартизации
    header = list(data[0])

    # Определяем индексы нужных колонок по их названиям
    dept_idx = header.index("department") if "department" in header else None
    name_idx = header.index("name") if "name" in header else None
    hours_idx = header.index("hours_worked") if "hours_worked" in header else None
    # Находим колонку с тарифом(должна быть последней не занятой. Только при условии, что нет дополнительных колонок)
    rate_idx = next(
        i for i, _ in enumerate(header) if i not in {dept_idx, name_idx, hours_idx}
    )  # создаем генератор пар(индекс, значение), если индекс переменной не находится в словаре с числами прошлых колонок, то он присваивается переменной
    # создаем новые данные со стандартной структурой
    standardized = []
    # начинаем итерация с 2 элемента, чтобы убрать ненужные нам заголовки
    for row in data[1:]:
        standardized.append(
            (row[dept_idx], row[name_idx], row[hours_idx], row[rate_idx])
        )

    return standardized


def read_csv(
    *paths: str,
) -> list:
    all_data = []
    for path in list(*paths):
        with open(path, "r") as file:
            results = []
            for line in file:
                line = line.strip()  # Удаляем все пробелы и переносы
                if line:  # Пропускаем пустые строки
                    results.append(tuple(line.split(",")))
            data = remove_columns(results, ["id", "email"])
            all_data.extend(standardize_structure(data))

    return all_data
