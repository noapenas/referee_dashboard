import uuid
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.users import Referee  # Importamos o modelo do árbitro

class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # O coração da escalabilidade: a quem pertence este jogo?
    ref_id = Column(UUID(as_uuid=True), ForeignKey("referees.id"), nullable=False, index=True)
    
    # Dados extraídos diretamente da FPF
    fpf_match_id = Column(String, index=True)  # Ex: "123456" do portal da FPF
    competition_name = Column(String)          # Ex: "1ª Divisão Distrital"
    match_date = Column(Date)
    
    # Equipas
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    
    # Contexto e Resultado
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    status = Column(String, default="Scheduled") # Scheduled, Completed, Cancelled
    
    # Relação para facilitar extração conjunta no Python
    referee = relationship("Referee", backref="matches")