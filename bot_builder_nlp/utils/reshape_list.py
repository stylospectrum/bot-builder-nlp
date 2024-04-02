def reshape_list(original_list: list, n: int, m: int):
    if len(original_list) != n * m:
        raise ValueError(
            "The new size does not match the number of elements in the list."
        )

    reshaped_list: list[float] = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(original_list[i * m + j])
        reshaped_list.append(row)

    return reshaped_list
