from mixin.rows import MultipleRows


def print_rows(rows: MultipleRows):
    print('multiple_row', rows)
    print("List of all rows (Keys) : ", [multiple_row.key for multiple_row in rows.all])
    print("List of all rows (Data) : ", [multiple_row.data for multiple_row in rows.all])
    print("First row        (Keys) : ", rows.first.key)
    print("First row        (Data) : ", rows.first.data)
