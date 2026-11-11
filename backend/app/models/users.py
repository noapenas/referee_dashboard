import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Referee(Base):
    __tablename__ = "referees"

    # UUID garante segurança total num ambiente com múltiplos árbitros
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    
    # ID da Associação (ex: 219 para AF Lisboa, útil para a API da FPF)
    association_id = Column(String, nullable=True) 
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)