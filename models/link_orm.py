from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates
from models.scheme import Base


class LinkOrm(Base):
    __tablename__ = 'links'
    id = Column(Integer, name='id', nullable=False, unique=True, primary_key=True, autoincrement=True)
    url = Column(String(1000), name='url', nullable=False)
    value = Column(String(100), name='value')
    prev_value = Column(String(100), name='prev_value')
    is_active = Column(Boolean, name='is_active', default=True)

    @validates('url', 'value', 'prev_value')
    def strip_value(self, key, value):
        if isinstance(value, str):
            return value.strip()
        return value

    def __repr__(self):
        return "<LinkOrm({id}, {url})>".format(id=self.id, url=self.url)
