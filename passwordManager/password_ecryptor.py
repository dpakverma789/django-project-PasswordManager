import string


def text_encryption(plain_text, salt='ec2'):
    encrypted_plain_text = ''
    try:
        for i in plain_text:
            if i.isalpha():
                ascii_text = ord(i)
                hex_text = hex(ascii_text)
            elif i.isnumeric():
                hex_text = hex(int(i))
            else:
                ascii_text = ord(i)
                hex_text = hex(ascii_text)
            encrypted_plain_text += hex_text[2:] + salt
    except:
        encrypted_plain_text = plain_text
    finally:
        return encrypted_plain_text


def text_decryption(encrypted_text_received):
    original_plain_text = ''
    salt = encrypted_text_received[-3:]
    encrypted_text_body = encrypted_text_received.split(salt)[:-1]
    is_done = False
    special_characters = ''.join((string.punctuation, ' '))
    for x in encrypted_text_body:
        concat_data = int(x, 16)
        decrypted_char = chr(int(concat_data))
        if decrypted_char.isalpha():
            ascii_pass_decrypt = str(decrypted_char)
            original_plain_text += ascii_pass_decrypt
        elif decrypted_char in special_characters:
            ascii_pass_decrypt = str(decrypted_char)
            original_plain_text += ascii_pass_decrypt
        else:
            original_plain_text += str(concat_data)
        is_done = True
    if is_done:
        return original_plain_text
    else:
        original_plain_text = encrypted_text_received
        return original_plain_text


