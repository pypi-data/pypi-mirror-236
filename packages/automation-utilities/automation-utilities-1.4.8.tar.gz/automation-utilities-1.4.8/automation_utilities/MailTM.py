import time

from names import get_first_name
from requests import JSONDecodeError
import requests
import random
from automation_utilities import Exceptions
from automation_utilities.Generator import generate_email, generate_password, generate_username

domains = [element['domain'] for element in requests.get('https://api.mail.tm/domains').json()['hydra:member']]


class Account:

    def __init__(
            self,
            name: str | None = None,
            username: str | None = None,
            password: str | None = None,
            username_length: int | None = None,
            password_length: int | None = None
    ):
        self.password = password if password is not None else generate_password(
            password_length if password_length is not None else random.randint(10, 15)
        )
        self.name = name if name is not None else get_first_name()
        self.username = username if username is not None else generate_username(
            get_first_name(), username_length if username_length is not None else random.randint(10, 15)
        )
        self.email_address = generate_email(random.choice(domains), name, username, username_length)

        data = {
            'address': self.email_address.lower(),
            'password': self.password
        }
        while True:
            try:
                response = requests.post('https://api.mail.tm/accounts', json=data).json()
                self.id = response['id']
                break
            except KeyError:
                raise Exceptions.AccountError()
            except JSONDecodeError:
                pass
        while True:
            try:
                token = requests.post('https://api.mail.tm/token', json=data).json()['token']
                break
            except JSONDecodeError:
                pass
        self.headers = {'Authorization': f"Bearer {token}"}

    def messages(self, timeout: float = 30):
        start = time.time()
        while True:
            while True:
                try:
                    resoponse = requests.get('https://api.mail.tm/messages', headers=self.headers).json()
                    break
                except JSONDecodeError:
                    pass
                if time.time() - start > timeout:
                    raise TimeoutError
            if resoponse['hydra:totalItems'] > 0:
                messages = []
                for member in resoponse['hydra:member']:
                    url = f'https://api.mail.tm/messages/{member["id"]}'
                    while True:
                        try:
                            messages.append(requests.get(url, headers=self.headers).json()['html'])
                            break
                        except JSONDecodeError:
                            pass
                if resoponse['hydra:totalItems'] == 1:
                    return messages[0][0]
                else:
                    return messages[0]
            if time.time() - start > timeout:
                raise TimeoutError
