import random
import string
from names import get_first_name


def generate_username(name: str = get_first_name(), length: int = random.randint(10, 15)):
    return f'{name}{"".join(random.choice(string.digits) for _ in range(length - len(name)))}'.lower()


def generate_email(
        domain: str,
        name: str | None = None,
        username: str | None = None,
        username_length: int | None = None
):
    if username is None:
        username = generate_username(
            name if name is not None else get_first_name(),
            username_length if username_length is not None else random.randint(10, 15)
        )
    return f'{username}@{domain}'


def generate_password(length: int = random.randint(10, 20)):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
