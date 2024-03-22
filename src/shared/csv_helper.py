def delete_row(fn: str, rows: int | str | list[int | str]) -> bool:
    if isinstance(rows, int) or rows.isdigit():
        lines = [int(rows)]
    elif isinstance(rows, list):
        lines = set(rows)
        lines = [int(row) for row in lines if isinstance(row, int) or row.isdigit()]
        lines = lines.sort()
    else:
        return False

    with open(fn, 'r+') as file:
        file_lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line_num, line in enumerate(file_lines):
            if line_num not in lines:
                file.write(line)

    return True


def conditional_delete_row(fn: str, match: str) -> bool:
    with open(fn, 'r+') as file:
        file_lines = file.readlines()
        file.seek(0)
        file.truncate()

        match = match.strip()
        for line_num, line in enumerate(file_lines):
            if line.strip() == match:
                continue
            file.write(line)

    return True