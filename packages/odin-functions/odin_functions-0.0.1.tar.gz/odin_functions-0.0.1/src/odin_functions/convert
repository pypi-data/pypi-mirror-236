def to_num(value):
    if isinstance(value,(int,float)):
        return value
    elif isinstance(value,str):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return 0
    elif value in [None,[] ,{}]:
        return 0
    
    return 0

# if __name__ == "__main__":
#     value = "0000000001"
#     print(f'input value type is : {type(value).__name__}')
#     print(f'converted value is {to_num(value)} and type is : {type(to_num(value)).__name__}')
