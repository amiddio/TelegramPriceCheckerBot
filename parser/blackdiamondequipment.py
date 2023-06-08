from bs4 import BeautifulSoup
from parser.parser_base import ParserBase


class Blackdiamondequipment(ParserBase):

    def parse(self, url: str) -> str | None:
        """
        Метод парсинга класса

        :param url: str
        :return: str | None
        """

        soup: BeautifulSoup = self.get_html_parser(url)
        if not soup:
            return

        res = soup.find('span', class_='low-regular-price')
        if res:
            return res.text.strip()

    def parse_title(self, url: str) -> str | None:
        """
        Парсим название продукта

        :param url: str
        :return: str | None
        """

        soup: BeautifulSoup = self.get_html_parser(url)
        if not soup:
            return

        res = soup.find('h1', class_='product-title')
        if res:
            return res.text.strip()
