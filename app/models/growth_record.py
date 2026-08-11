from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from app.core.database import Base


class GrowthRecord(Base):
    __tablename__ = "growth_records"

    id = Column(Integer, primary_key=True, index=True)
    plantation_id = Column(Integer, ForeignKey("plantations.id"), nullable=False)
    height = Column(Float, nullable=False)
    recorded_date = Column(Date, nullable=False)