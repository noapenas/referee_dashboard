from fastapi import FastAPI
from app.api import v1_garmin
# from app.core.database import engine, Base 
# (Vamos descomentar a linha acima quando ligarmos o Docker/PostgreSQL)

app = FastAPI(
    title="Referee Dashboard API", 
    description="API para gestão de dados físicos, técnicos e disciplinares de arbitragem",
    version="1.0.0"
)

# Registar as rotas da nossa aplicação
app.include_router(v1_garmin.router, prefix="/api/v1/garmin", tags=["Integração Garmin"])

@app.get("/")
def read_root():
    return {"status": "online", "message": "Referee Dashboard API está a correr!"}