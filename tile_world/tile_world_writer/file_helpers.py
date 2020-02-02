
BYTE_SIZE = 1
WORD_SIZE = 2
LONG_SIZE = 4

def placeholder(data, placeholder_size):
    offset = len(data)
    wb(data, 0, placeholder_size)
    return (offset, placeholder_size)


def fill_placeholder(data, placeholder, is_relative=True):
    if is_relative:
        data_value = get_data_size_after_placeholder(data, placeholder)
    else:
        data_value = len(data)
    wb(data, data_value, placeholder[1], placeholder[0])


def get_data_size_after_placeholder(data, placeholder):
    data_len = len(data)
    data_size = data_len - placeholder[0] - placeholder[1]
    return data_size


def wb(data, value, byte_size, index = -1):
    bytes_value = int(value).to_bytes(byte_size, byteorder='little', signed=False)
    if index == -1:
        for byte in bytes_value:
            data.append(byte)
    else:
        for i, byte in enumerate(bytes_value):
            data[index + i] = byte