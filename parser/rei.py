from bs4 import BeautifulSoup
from parser.parser_base import ParserBase


class Rei(ParserBase):

    def parse(self, url: str) -> str | None:
        """
        Метод парсинга класса

        :param url: str
        :return: str | None
        """

        soup: BeautifulSoup = self.get_html_parser(url)
        if not soup:
            return

        res = soup.find('span', id='buy-box-product-price')
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

        res = soup.find('h1', id='product-page-title')
        if res:
            return res.text.strip()
