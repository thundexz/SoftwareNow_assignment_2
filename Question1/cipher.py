# dividing the letter into first half and second half
LOWER_FIRST = "abcdefghijklmn"      
LOWER_SECOND = "opqrstuvwxyz"      
UPPER_FIRST = "ABCDEFGHIJKLM"        
UPPER_SECOND = "NOPQRSTUVWXYZ"       
DIGITS = "0123456789"             


#fn shifting character forward by `shift` positions inside `group`, wrapping around.
def _shift_within(ch, group, shift):
    idx = group.index(ch)
    new_idx = (idx + shift) % len(group)
    return group[new_idx]


#fn encrypting a single character according to given rule.
def encrypt_char(ch, shift1, shift2):
    if ch.islower():
        # for a-n, shifting forward
        if ch in LOWER_FIRST:  
            return _shift_within(ch, LOWER_FIRST, shift1 * shift2)
        # for o-z, shifting backward
        else:  
            return _shift_within(ch, LOWER_SECOND, -(shift1 + shift2))

    if ch.isupper():
        if ch in UPPER_FIRST: 
            # for A-M, shifting backward
            return _shift_within(ch, UPPER_FIRST, -shift1)
        else:  
            # for N-Z, shifting forward
            return _shift_within(ch, UPPER_SECOND, shift2 ** 2)

    if ch.isdigit():
        # for digit shifting forward
        return _shift_within(ch, DIGITS, shift1 - shift2)
    # for special charater, spaces and other returning same
    return ch


#fn decrypting encrypted character using reversed rules as above encrypted.
def decrypt_char(ch, shift1, shift2):
    if ch.islower():
        if ch in LOWER_FIRST:
            return _shift_within(ch, LOWER_FIRST, -(shift1 * shift2))
        else:
            return _shift_within(ch, LOWER_SECOND, shift1 + shift2)

    if ch.isupper():
        if ch in UPPER_FIRST:
            return _shift_within(ch, UPPER_FIRST, shift1)
        else:
            return _shift_within(ch, UPPER_SECOND, -(shift2 ** 2))

    if ch.isdigit():
        return _shift_within(ch, DIGITS, -(shift1 - shift2))

    return ch


