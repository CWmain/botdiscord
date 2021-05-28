def HextoAscii(hex):
    """
    Given a hexidecimal input as a string, coverts it to an ASCII string
    """
    list_hex = hex.split('\\x')
    print(HextoInt(list_hex))


def HextoInt(list_hex):
    '''
    Given a list of hexidecimal, converts it to list of integers
    '''
    list_int = []
    for hex in list_hex:
        try:
            list_int.append(int(hex, 16))
        except:
            list_int.append(hex)

    return list_int
