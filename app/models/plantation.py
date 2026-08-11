from sqlalchemy import Column, Integer, Date, ForeignKey

from app.core.database import Base


class Plantation(Base):
    __tablename__ = "plantations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tree_id = Column(Integer, ForeignKey("trees.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    planting_date = Column(Date, nullable=False)