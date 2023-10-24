from phonenumbers import region_code_for_number, parse


class PhoneNumber:
    def __init__(self, phone_number):
        self.number = phone_number
        parsed_number = parse(f'+{phone_number}')
        self.prefix = parsed_number.country_code
        self.country = region_code_for_number(parsed_number)
