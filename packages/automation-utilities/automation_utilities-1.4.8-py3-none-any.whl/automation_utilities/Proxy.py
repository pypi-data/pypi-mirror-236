class Proxy:
    def __init__(
            self, text: str
    ):
        self.text = text
        try:
            self.authintication_information, self.server = text.split('@')
        except ValueError:
            self.username = self.password = None
            self.server = text

    def for_requests(self):
        server = f'http://{self.text}'
        return {"http": server, 'https': server}

    def for_playwright(self):
        try:
            username, password = self.authintication_information.split(':')
            return {
                'server': f'http://{self.server}',
                'username': username,
                'password': password,
            }
        except AttributeError:
            return {
                'server': f'http://{self.server}'
            }
