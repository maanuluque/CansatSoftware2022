__MASK = 0xFF
__MASK_NUM_BITS = 8

def int_to_bytes(number):
    byte_array = bytearray()
    byte_array.append(number & __MASK)
    number >>= __MASK_NUM_BITS
    
    while number != 0:
        aux = bytearray()
        aux.append(number & __MASK)
        byte_array = aux + byte_array
        number >>= __MASK_NUM_BITS
    
    return byte_array

def int_to_length(number):
    length = int_to_bytes(number)
    if len(length) < 2:
        aux = bytearray(1)
        length = aux + length
    return length