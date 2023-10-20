def type_name(value):
    dictionary = {
        "int": False,
        "float": False,
        "str": False,
        "bool": False,
        "list": False,
        "tuple": False,
        "set": False,
        "dict": False,
        "NoneType": False
    }

    for key in dictionary:
        if type(value).__name__ == key:
            dictionary[key] = True

    return dictionary

# if __name__ == "__main__":
    # value = 1
    # type_name(value)
    # int

    # value = 1.1
    # type_name(value)
    # # float

    # value = "abc"
    # type_name(value)
    # # str

    # value = False
    # type_name(value)
    # # bool

    # value = [1,2,3]
    # type_name(value)
    # # list

    # value = (1,2,3)
    # type_name(value)
    # # tuple

    # value = {"key":"value"}
    # type_name(value)
    # # dict

    # value = {1,2,3}
    # type_name(value)
    # # set

    # value = None
    # type_name(value)
    