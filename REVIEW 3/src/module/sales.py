from sqlalchemy import Column, Integer, Date, ForeignKey, Numeric
from module.base import Base

class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    sale_date = Column(Date, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    revenue = Column(Numeric, nullable=False)


