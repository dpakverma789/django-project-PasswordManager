import random
import string


def text_encryption(plain_text, salt='357'):
    encrypted_plain_text = ''
    try:
        for i in plain_text:
            salt = int(salt) + 3
            if i.isalpha():
                ascii_text = ord(i)
                hex_text = hex(ascii_text)
            elif i.isnumeric():
                digit = int(i) * len(str(salt))
                hex_text = hex(int(digit))
            else:
                ascii_text = ord(i)
                hex_text = hex(ascii_text)
            encrypted_plain_text += hex_text[2:] + str(salt)
    except Exception as e:
        print(e)
        encrypted_plain_text = plain_text
    finally:
        return encrypted_plain_text


def text_decryption(encrypted_text_received):
    original_plain_text = decrypted_char = ''
    salt = encrypted_text_received[-3:]
    for idx, _ in enumerate(encrypted_text_received):
        salt = salt if idx == 0 else int(salt) - 3
        encrypted_text_received = encrypted_text_received.replace(str(salt), '.')
    encrypted_text_body = encrypted_text_received.split('.')
    encrypted_text_body.pop()
    is_done = False
    special_characters = string.punctuation
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
            digit = int(concat_data) / len(str(salt))
            original_plain_text += str(int(digit))
        is_done = True
    if is_done:
        return original_plain_text
    else:
        original_plain_text = encrypted_text_received
        return original_plain_text


key = random.randint(100, 999)

# if __name__ == '__main__':
#     text = input('Enter your TexT: ')
#     flag = True
#     while flag:
#         key = random.randint(100, 999)
#         encrypted_text = text_encryption(plain_text=text, salt=key)
#         try:
#             decrypted_text = text_decryption(encrypted_text_received=encrypted_text)
#         except:
#             continue
#         else:
#             print(encrypted_text, '\n')
#             flag = False
#     encrypted_text = input('Enter your Encrypted TexT: ')
#     decrypted_text = text_decryption(encrypted_text_received=encrypted_text)
#     print(decrypted_text,'\n')