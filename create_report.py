def create_file(
    name: str,
    data: str,
) -> None:
    with open(file=name, mode="w+", encoding="UTF-8") as file:
        file.write(data)
        print(data)
        file.close()
