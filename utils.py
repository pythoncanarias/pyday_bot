#!/usr/binenv python

_map_first_numbers = {
    'cero': 0, 'zero': 0,
    'uno': 1, 'one': 1,
    'dos': 2, 'two': 2,
    'tres': 3, 'three': 3,
    'cuatro': 4, 'four': 4,
    'cinco': 5, 'five': 5,
    'seis': 6, 'six': 6,
    'siete': 7, 'seven': 7,
    'ocho': 8, 'eight': 8,
    'nueve': 9, 'nine': 9,
    'diez': 10, 'ten': 10,
    'once': 11, 'eleven': 11,
    'doce': 12, 'twelve': 12,
    }


def as_integer(value):
    global _map_first_numbers
    if isinstance(value, int):
        return True, value
    if isinstance(value, float):
        if int(value) == value:
            return True, int(value)
        else:
            return False, value
        return True, value
    if isinstance(value, str) and value in _map_first_numbers:
        return True, _map_first_numbers[value]
    try:
        i = int(str(value))
        return True, i
    except ValueError:
        pass
    return False, value

