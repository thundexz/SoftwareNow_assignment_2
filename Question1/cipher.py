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


# fn that read raw_text.txt file and encrypt content 
def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    encrypted = "".join(encrypt_char(c, shift1, shift2) for c in text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encrypted)

# fn that read encrypted_text.txt file and decrypt content 
def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads from input_path (encrypted_text.txt) and writes decrypted content to output_path."""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    decrypted = "".join(decrypt_char(c, shift1, shift2) for c in text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decrypted)

# fn comparing the raw_text.txt and decrypted_text.txt, inorder to verify that both file match the content
def verify_files(original_path: str, decrypted_path: str) -> bool:
    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()

    with open(decrypted_path, "r", encoding="utf-8") as f:
        decrypted = f.read()

    success = original == decrypted

    if success:
        print("Decryption successful: files match.")
    else:
        print("Decryption failed: files do not match.")
    return success


def main():
    shift1 = int(input("Enter shift1 (non-negative integer): "))
    shift2 = int(input("Enter shift2 (non-negative integer): "))

    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
    decrypt_file(shift1, shift2, "encrypted_text.txt", "decrypted_text.txt")
    verify_files("raw_text.txt", "decrypted_text.txt")


if __name__ == "__main__":
    main()

