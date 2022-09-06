
def pass_encrypt(simple_text, encrypted_password='', key='q5e2c'):
    try:
        for i in simple_text:
            if i.isalpha():
                ascii_pass_encrypt = ord(i)
                binary_pass = hex(ascii_pass_encrypt)
            elif i.isnumeric():
                binary_pass = hex(int(i))
            else:
                ascii_pass_encrypt = ord(i)
                binary_pass = hex(ascii_pass_encrypt)
            encrypted_password += binary_pass[2:] + key
    except:
        encrypted_password = simple_text
    finally:
        return encrypted_password


def pass_decrypt(password_Encrypted, key='q5e2c'):
    splited_password = password_Encrypted.split(key)[:-1]
    return loopKey(splited_password,password_Encrypted)


def loopKey(splited_password, password_Encrypted, orignal_password=''):
    sample = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-']
    sample2 = ['_', '+', '=', ' ', '[', ']', '{', '}', '"', "'"]
    is_done = False
    for x in splited_password:
        concat_data = int(x, 16)
        flag = chr(int(concat_data))
        if flag.isalpha():
            ascii_pass_decrypt = str(flag)
            orignal_password += ascii_pass_decrypt
        elif flag in sample or flag in sample2:
            ascii_pass_decrypt = str(flag)
            orignal_password += ascii_pass_decrypt
        else:
            orignal_password += str(concat_data)
        is_done = True
    if is_done:
        return orignal_password
    else:
        orignal_password = password_Encrypted
        return orignal_password