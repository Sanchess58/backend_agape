import hashlib
import random
import re
import string


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def generate_password() -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(16))
    return hash_password(password)


def is_password_correct(password: str) -> bool:
    return bool(re.fullmatch(r"?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}", password))
