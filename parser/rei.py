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
