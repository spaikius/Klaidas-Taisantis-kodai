#!/usr/bin/env python

import sys
import binascii

__author__ = "Rimvydas Noreika"

def decode_message(encoded_message):
    if len(encoded_message) % 8 != 0:
        encoded_message = encoded_message[:-(len(encoded_message) % 8)]

    message_in_binary = int(encoded_message, 2)
    return binascii.unhexlify('%x' % message_in_binary)


def fix_errors(data, bite_orders, bite_to_swap_positions):
    fixed_data = list()

    for data_line in data:
        errors = list()
        for order in bite_orders:
            summ = 0
            for bite in order:
                summ += int(data_line[bite])
            errors.append(summ % 2)
        
        if sum(errors) > 1:
            indexes = [str(index) for index, error in enumerate(errors) if error == 1]
            key = ''.join(indexes)
            bites_list = list(data_line)

            wrong_bit = bites_list[bite_to_swap_positions[key]]
            correct_bit = "1" if wrong_bit == "0" else "0"

            bites_list[bite_to_swap_positions[key]] = correct_bit

            fixed_data.append(''.join(bites_list))
        else:
            fixed_data.append(data_line)

    return fixed_data


# -- Pirma uzduotis -- #
def _pirma_uzduotis(file):
    bite_orders = [
        [0, 1, 2, 3, 12],
        [4, 5, 6, 7, 13],
        [8, 9, 10, 11, 14],
        [0, 4, 8, 15],
        [1, 5, 9, 16],
        [2, 6, 10, 17],
        [3, 7, 11, 18]
    ]

    bite_to_swap_positions = {
        '03': 0, '04': 1, '05': 2, '06': 3,
        '13': 4, '14': 5, '15': 6, '16': 7,
        '23': 8, '24': 9, '25': 10, '26': 11
    }

    data = [line.rstrip('\n') for line in open(file)]

    fixed_data = fix_errors(data, bite_orders, bite_to_swap_positions)
    encoded_message = ''.join([line[:12] for line in fixed_data])
    
    return decode_message(encoded_message)


# -- 2 uzduotis
def _antra_uzduotis(file):
    bite_orders = [
        [0, 1, 2, 6],
        [3, 4, 7, 2],
        [5, 8, 4, 1],
        [9, 5, 3, 0]
    ]

    bite_to_swap_positions = {
        "01": 2, "02": 1, "03": 0,
        "12": 4, "13": 3,
        "23": 5
    }

    data = [line.rstrip('\n') for line in open(file)]
    
    fixed_data = fix_errors(data, bite_orders, bite_to_swap_positions)
    encoded_message = ''.join([line[:6] for line in fixed_data])
    return decode_message(encoded_message)


# -- 3 uzduotis
def _trecia_uzduotis(file):
    bite_orders = [
        [2, 4, 6, 0],
        [2, 5, 6, 1],
        [4, 5, 6, 3]
    ]

    bite_to_swap_positions = {
        '01': 2, '02': 4,
        '12': 5, 
        '012': 6 
    }

    data = [line.rstrip('\n') for line in open(file)]

    fixed_data = fix_errors(data, bite_orders, bite_to_swap_positions)
    encoded_message = ''
    for data_line in fixed_data:
        data_bites = list(data_line)
        encoded_message += ''.join([bite for index, bite in enumerate(data_bites) if index not in [0, 1, 3]])

    return decode_message(encoded_message)


# -- Main

if len(sys.argv) != 4:
    print("Pateik 3 failus. Aciu\n")
    exit()

print("5.1: {0}".format(_pirma_uzduotis(sys.argv[1])))
print("5.2: {0}".format(_antra_uzduotis(sys.argv[2])))
print("5.3: {0}".format(_trecia_uzduotis(sys.argv[3])))
