from ingestion_service.database import engine
from ingestion_service.models import Base

Base.metadata.create_all(bind=engine)

print("Database created successfully!")