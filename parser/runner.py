import re
from urllib.parse import urlparse
from lexicon.lexicon import LEXICON_GENERAL_RU
from models.link_model import LinkModel
from models.link_orm import LinkOrm
from parser.parser_base import ParserBase
# Каждый класс парсинга необходимо импортировать: {
from parser.amazon import Amazon
from parser.iherb import Iherb
from parser.rei import Rei
from parser.blackdiamondequipment import Blackdiamondequipment
# }


def run() -> list[LinkOrm]:
    """
    Метод осуществляет парсинг страницы продукта и определяет изменилась ли цена, или нет.
    Если изменилась - добавляем продукт в список, который потом возвращаем

    :return: list[LinkOrm]
    """

    result: list[LinkOrm] = []

    # Возвращаем список активных для парсинга ссылок на продукты
    links = LinkModel.get_all(fltr={'is_active': True})
    if not links:
        return result

    for item in links:
        # Определяем класс для парсинга
        klass = _get_class_name(item.url)
        if klass:

            # Если название продукта пустое пробуем его пропарсить и сохранить
            if not item.title:
                title = globals()[klass]().parse_title(item.url)
                if title:
                    item.title = title
                    LinkModel(item).save()

            # Парсим продукт и получаем цену
            price = globals()[klass]().parse(item.url)
            # Если продукт недоступен при первом парсинге переходим к другому элементу
            if not price and not item.value:
                continue
            # Если цена изменилась добавляем продукт в список
            # и сохраняем изменения в модели
            if price != item.value:
                # Сравниваем цены. Если разница меньше 1 то игнорируем изменения
                if _get_prices_diff(price, item.value):
                    item.prev_value = item.value
                    item.value = price
                    result.append(item)
                    LinkModel(item).save()
        else:
            raise AttributeError(LEXICON_GENERAL_RU["parser class not found"].format(url=item.url))
    return result


def get_message(link: LinkOrm) -> str:
    """
    Формируем сообщение для бота на основе данных ссылки

    :param link: LinkOrm
    :return: str
    """

    title = f"<b>{link.title}</b>\n" if link.title else ''
    v = f"{link.value}" if link.value else LEXICON_GENERAL_RU["not available"]
    pv = f"{link.prev_value}" if link.prev_value else LEXICON_GENERAL_RU["not available"]
    return LEXICON_GENERAL_RU["product changed"].format(title=title, prev=pv, curr=v, link=link.url)


def _get_class_name(url: str) -> str | None:
    """
    Динамическое поределение класса для парсинга на основе переданной ссылки

    :param url: str
    :return: str | None
    """

    # Получаем домэйн из ссылки
    domain: str = urlparse(url).netloc

    # Достаем дочерние классы от базового
    subclasses: list = ParserBase.__subclasses__()
    if not subclasses:
        return

    # Разбиваем домэйн по точкам
    domain_splited = domain.lower().split('.')
    for klass in subclasses:
        # Возвращаем название класса если его можно найти в домэйн
        if klass.__name__.lower() in domain_splited:
            return klass.__name__
    return


def _get_prices_diff(price1, price2):
    def get_num(n):
        return re.search(r"(\d+.?\d+)", n)

    # Находим цены в строках
    p1 = get_num(price1)
    p2 = get_num(price2)
    if p1 and p2:
        p1 = float(p1.group())
        p2 = float(p2.group())
        res = abs(p1 - p2)  # Получаем абсолютную разницу
        return True if res > 1 else False  # Если разница меньше 1 то игнорим
    return True
