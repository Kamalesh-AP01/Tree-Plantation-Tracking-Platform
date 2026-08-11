from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True, index=True)
    tree_name = Column(String, nullable=False)