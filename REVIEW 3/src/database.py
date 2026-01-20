from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Simran%401@localhost:5432/Market"

engine = create_engine(DATABASE_URL)
