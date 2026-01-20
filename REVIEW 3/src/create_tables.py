from database import engine
from module.base import Base
from module.products import Product
from module.sales import Sales

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully")
