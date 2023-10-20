import secrets

from pyrandomify.enums import Base


class Digits(Base):
    """
       A class that includes an automatic generation function
    """

    def generate(self, lenght: int = 6) -> str:
        """
        The function randomly selects a character from the list and generates a whole text
        :param lenght: Length of the future result
        :return: string
        """
        result = ''.join([secrets.choice(self.digits) for _ in range(lenght)])
        return result
