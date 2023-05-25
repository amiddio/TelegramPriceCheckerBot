from bs4 import BeautifulSoup
from parser.parser_base import ParserBase


class Amazon(ParserBase):

    __SELECTORS: list[dict[str, str]] = [
        {'id': 'corePrice_desktop', 'class': 'apexPriceToPay'},
        {'id': 'corePriceDisplay_desktop_feature_div', 'class': 'priceToPay'},
    ]

    def parse(self, url: str) -> str | None:
        """
        Парсим цену продукта

        :param url: str
        :return: str | None
        """

        soup: BeautifulSoup = self.get_html_parser(url)
        if not soup:
            return

        for item in self.__SELECTORS:
            css_id, css_class = item.values()
            price = Amazon._get_price(soup=soup, css_id=css_id, css_class=css_class)
            if price:
                return price.strip()

    def parse_title(self, url: str) -> str | None:
        """
        Парсим название продукта

        :param url: str
        :return: str | None
        """

        soup: BeautifulSoup = self.get_html_parser(url)
        if not soup:
            return

        res = soup.find('span', id='productTitle')
        if res:
            return res.text.strip()

    @staticmethod
    def _get_price(soup, css_id, css_class) -> str | None:
        res = soup.find('div', id=css_id)
        if res:
            price = res.select_one(f'span.{css_class} > span.a-offscreen')
            if price:
                return price.text
        return None

