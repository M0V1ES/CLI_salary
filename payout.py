def create_report_payout(
    csv: list,
) -> str:  # создание отчета по зарплатам
    dict_payload = {}
    dict_humans = {}
    for count, items in enumerate(csv):
        human_key = items[1]
        hours = items[2]
        rate = items[3]
        payout = int(items[2]) * int(items[3])
        # если в словаре с именами нет имени
        if human_key not in dict_humans:
            dict_humans[human_key] = [
                hours,
                rate,
                payout,
            ]

        department = items[0]
        # если в словаре с департаментами нет департамента
        if department not in dict_payload:
            dict_payload[department] = {}

        # Добавляем данные сотрудника в отделе
        dict_payload[department][human_key] = dict_humans[human_key]

    # вывод
    output = ""
    output += (
        "name".rjust(10)
        + "hours".rjust(17)
        + "rate".rjust(10)
        + "payout".rjust(10)
        + "\n"
    )
    for i, human in dict_payload.items():
        total_hours = 0
        total_salary = 0
        output += i + "\n"
        for name, data in human.items():
            hours, rate, salary = data
            total_hours += int(hours)
            total_salary += int(salary)
            output += (
                "-" * 5
                + name.ljust(15)
                + hours.rjust(5)
                + rate.rjust(10)
                + f"${salary}".rjust(10)
                + "\n"
            )
        output += f"{total_hours}".rjust(25) + f"${total_salary}".rjust(20) + "\n"
    return output
