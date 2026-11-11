from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.services.garmin_parser import parse_fit_file

router = APIRouter()

@router.post("/upload")
async def upload_garmin_file(file: UploadFile = File(...)):
    # Validação simples de segurança
    if not file.filename.lower().endswith('.fit'):
        raise HTTPException(status_code=400, detail="O ficheiro tem de ser no formato .FIT")
    
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # 1. Guardar o ficheiro temporariamente
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Chamar o nosso motor de extração (que construímos no passo anterior)
        stats = parse_fit_file(temp_file_path)
        
        # Nota de Arquitetura: Numa fase posterior, em vez de devolver logo os dados,
        # vamos gravar o 'stats' na Base de Dados (PhysicalStats) associado ao ref_id.
        return {"status": "sucesso", "data": stats}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar ficheiro: {str(e)}")
    
    finally:
        # 3. Limpeza: apagar o ficheiro temporário para não ocupar espaço
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)