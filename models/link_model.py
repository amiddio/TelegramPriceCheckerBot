from sqlalchemy import desc, asc, and_, func
from logger.logger import log
from models.link_orm import LinkOrm
from models.scheme import session


class LinkModel:
    _orm: LinkOrm = None

    def __init__(self, orm: LinkOrm) -> None:
        self._orm = orm

    def save(self) -> LinkOrm | None:
        """
        Метод сохраняет изменения в ORM модели в БД

        :return: LinkOrm | None
        """

        try:
            session.add(self._orm)
            session.commit()
            session.refresh(self._orm)
            return self._orm
        except Exception as e:
            log().error(str(e))
            session.rollback()

    def delete(self) -> None:
        """
        Метод удаляет ORM из БД

        :return: None
        """

        try:
            session.delete(self._orm)
            session.commit()
        except Exception as e:
            log().error(str(e))
            session.rollback()

    @staticmethod
    def get_one(iid: int) -> LinkOrm:
        """
        Возвращает ORM запись по айди

        :param iid: int
        :return: LinkOrm
        """

        return session.query(LinkOrm).filter(LinkOrm.id == iid).first()

    @staticmethod
    def get_all(fltr: dict = None) -> list[LinkOrm]:
        """
        Возвращает список ORM найденых записей, согласно фильтру

        :param fltr: dict
        :return: list[LinkOrm]
        """

        query = session.query(LinkOrm).order_by(asc(LinkOrm.id))
        if fltr:
            filter_expression = [func.lower(getattr(LinkOrm, k)) == func.lower(v) for k, v in fltr.items()]
            query = query.filter(and_(*filter_expression))
        return query.all()
