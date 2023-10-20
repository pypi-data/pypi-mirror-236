from typing import List


def binary_search(sorted_list: List[int], number: int) -> int:
    lower_bound = 0
    upper_bound = len(sorted_list)

    if not sorted_list or number < sorted_list[0] or number > sorted_list[-1]:
        # Out of range of contents in collection
        return -1

    while lower_bound != upper_bound:
        index = (upper_bound + lower_bound) // 2

        if number == sorted_list[index]:
            return index
        elif number > sorted_list[index]:
            if lower_bound == index:
                break
            lower_bound = index
        # elif number < sorted_list[index]:
        else:
            if upper_bound == index:
                break
            upper_bound = index

    return -1


def binary_search2(sorted_list: List[int], number: int) -> int:
    lower_bound = 0
    upper_bound = len(sorted_list)

    if not sorted_list or number < sorted_list[0] or number > sorted_list[-1]:
        # Out of range of contents in collection
        return -1

    while lower_bound != upper_bound:
        index = (upper_bound + lower_bound) // 2
        current_item = sorted_list[index]

        if number == current_item:
            return index
        elif number > current_item:
            if lower_bound == index:
                break
            lower_bound = index
        elif number < current_item:
            if upper_bound == index:
                break
            upper_bound = index

    return -1
