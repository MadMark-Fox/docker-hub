import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Ansible Visual API")

# Directorio donde se guardan los playbooks (según tu docker-compose y Dockerfile)
PLAYBOOK_DIR = "/opt/ansible-visual/api/playbooks"

# Asegurar que el directorio existe
os.makedirs(PLAYBOOK_DIR, exist_ok=True)

# Modelo de datos para recibir el playbook desde el frontend
class PlaybookRequest(BaseModel):
    filename: str
    content: str

@app.get("/")
def root():
    return {"message": "Ansible Visual API lista para trabajar"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 1. Listar los archivos disponibles
@app.get("/playbooks")
def list_playbooks():
    files = [f for f in os.listdir(PLAYBOOK_DIR) if f.endswith(".yml") or f.endswith(".yaml")]
    return {"playbooks": files}

# 2. Leer el contenido de un playbook específico
@app.get("/playbooks/{filename}")
def get_playbook(filename: str):
    file_path = os.path.join(PLAYBOOK_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Playbook no encontrado")
    
    with open(file_path, "r") as f:
        content = f.read()
    return {"filename": filename, "content": content}

# 3. Guardar (Crear o Editar) un playbook
@app.post("/playbooks")
def save_playbook(playbook: PlaybookRequest):
    # Evitar guardar fuera del directorio permitido
    if ".." in playbook.filename or "/" in playbook.filename:
         raise HTTPException(status_code=400, detail="Nombre de archivo inválido")

    file_path = os.path.join(PLAYBOOK_DIR, playbook.filename)
    
    # Si no termina en .yml, se lo agregamos
    if not file_path.endswith(".yml"):
        file_path += ".yml"

    with open(file_path, "w") as f:
        f.write(playbook.content)
    
    return {"message": f"Playbook {playbook.filename} guardado correctamente"}

# 4. Ejecutar el playbook usando Ansible
@app.post("/playbooks/{filename}/run")
def run_playbook(filename: str):
    file_path = os.path.join(PLAYBOOK_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Playbook no encontrado")

    try:
        # Ejecutamos ansible-playbook sobre el archivo
        # 'localhost,' y '--connection=local' son para probar sin inventario externo
        result = subprocess.run(
            ["ansible-playbook", file_path, "--connection=local", "-i", "localhost,"],
            capture_output=True,
            text=True
        )
        
        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"error": str(e)}