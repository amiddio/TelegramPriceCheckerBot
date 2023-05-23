from bs4 import BeautifulSoup
from parser.parser_base import ParserBase


class Iherb(ParserBase):

    def parse(self, url: str) -> str | None:
        """
        Метод парсинга класса

        :param url: str
        :return: str | None
        """
        
        soup: BeautifulSoup = self.get_html_parser(url)
        if not soup:
            return

        res = soup.find('div', class_='price-inner-text')
        if res:
            return res.text.strip()
