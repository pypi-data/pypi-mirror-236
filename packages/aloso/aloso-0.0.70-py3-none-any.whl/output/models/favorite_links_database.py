from sqlalchemy import Column, Integer, String

from domain.favorite_links import FavoriteLinks
from output.database.database_base import Base


class FavoriteLinksData(Base, FavoriteLinks):
    __tablename__ = "FavoriteLinks"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(50))
