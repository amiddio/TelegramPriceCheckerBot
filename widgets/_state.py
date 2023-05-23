from models.link_orm import LinkOrm


class State:
    """
    Класс-контейнер для передачи состояния между различными страницами.
    Например, чтоб из списка перейти на форму и потом вернуться опять к списку
    """

    STATE_FORM = 'FORM'
    STATE_LIST = 'LIST'

    def __init__(self, iid: str, back: str) -> None:
        self.id = iid
        self.back = back
        self.row: LinkOrm | None = None

    @property
    def row(self) -> LinkOrm:
        return self._row

    @row.setter
    def row(self, value: LinkOrm) -> None:
        self._row = value
