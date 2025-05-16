import re


class Formatter:
    @staticmethod
    def format_value(value: str) -> int:
        """
        Converts a formatted number string into an integer.

        Removes a spaces, commas, and dots before conversion.

        :param value: A string representing a number (e.g., "1 000 000", "1.000.000").
        :return: An integer representation of the input.
        """
        value = value.replace(" ", "").replace(",", "").replace(".", "")
        return int(value)

    @staticmethod
    def format_month(month: int) -> str:
        return f"{month:02}"

    @staticmethod
    def format_number_with_spaces(number: int) -> str:
        return f"{number:,}".replace(",", " ")


class Validator:
    @staticmethod
    def is_valid_link(url: str) -> bool:
        """
         Checks if a URL contains "mdmcar.com/car".

        :param url: The URL string to validate.
        :return: True if the URL contains "mdmcar.com/car", otherwise False.
        """
        patterns = [
            r'^(https?://)?(mdmcar\.com)/car/\d+$',
            r'^(https?://)?(fem\.|www\.)?encar\.com(/.*)?$'
        ]
        return any(re.match(pattern, url) for pattern in patterns)

    @staticmethod
    def get_site_name(url: str) -> str:
        if re.search(r'(https?://)?mdmcar\.com', url):
            return "mdmcar"
        elif re.search(r'(https?://)?(www\.|fem\.)?encar\.com', url):
            return "encar"
        return "unknown"

    @staticmethod
    def is_valid_value(value: str) -> bool:
        """
        Checks if a string consists only of digits and spaces.

        Dots are ignored before validation.

        :param value: The input string.
        :return: True if the string contains only digits and spaces, otherwise False.

        **Examples**:
            "123 456" -> True \n
            "12.34" -> True  (dots are removed before checking) \n
            "123,4" -> True (commas are removed before checking) \n
            "12a34" -> False
        """
        value = value.replace(".", "").replace(",", "")
        return bool(re.match(r'^[0-9 ]+$', value))
