import numpy as np

'''
created and maintained by rifqi khairur rahman
current version is 0.0.4
'''


def split(self, array=[], x_length=0, y_length=0, xy_shift=0, repeat=False):

    x_return = []
    y_return = []


    # sanitation checking, if entries is impossible
    if array is []:
        raise ValueError("array should be exists, can't be none or []")

    if (x_length < 1) or (y_length < 1) :
        raise ValueError("x_length or y_length, cannot less than 1")

    if (x_length > len(array)) or (y_length >len(array)):
        raise ValueError("x_length or y_length cannot bigger than length of the array itself")

    if (xy_shift > len(array)) or (xy_shift < len(array)*-1):
        raise ValueError("xy_shift cannot bigger than array length or less than negative of the array length")

    # --------------------------------------------------------------------------------------------------------------

    size = 0
    if xy_shift >= 0:
        if x_length == y_length:
            size = x_length + xy_shift
            print("size = x_length + xy_shift")
        elif x_length >= y_length + xy_shift:
            size = x_length
            print("size = x_length")
        elif x_length < y_length+xy_shift:
            size = y_length + xy_shift
            print("size = y_length + xy_shift")
    elif xy_shift < 0:
        if x_length > y_length or x_length == y_length:
            size = x_length + abs(xy_shift)
            print("size = x_length + |xy_shift|")
        elif y_length > x_length:
            size = y_length + abs(xy_shift)
            print("size = y_length + |xy_shift|")

    # STEP 2 , split if repeat or not ------------------------------------------------------------------------------
    array_data = []

    if not repeat:
        array_data = np.split(array, np.arange(size, len(array), size))

        # delete last item in array because  it's just rest data with length that not same size with others
        if len(array_data[-1]) != size:
            array_data.pop()
    elif repeat:
        ret = []
        for index in range(0, len(array) - size + 1):
            ret.append(array[index:index + size])
        array_data = ret

    # XY selection
    if xy_shift >= 0:
        x_return = [i[:x_length] for i in array_data]  # grab x
        y_return = [i[xy_shift:xy_shift+y_length] for i in array_data]  # grab y
    elif xy_shift < 0:
        y_return = [i[:y_length] for i in array_data]  # grab x
        x_return = [i[xy_shift*-1:xy_shift*-1 + x_length] for i in array_data]  # grab y

    return x_return, y_return
