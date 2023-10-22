import random

def PasswordGenerate(length=12, use_digits=True, use_special_chars=True):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if use_digits:
        characters += '0123456789'
    if use_special_chars:
        characters += '!@#$%^&*()_+-=[]{}|;:,.<>?'

    password = ''.join(random.choice(characters) for _ in range(length))
    return password
