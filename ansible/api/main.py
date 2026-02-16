from fastapi import FastAPI

app = FastAPI(title="Ansible Visual API")


@app.get("/")
def root():
    return {"message": "Ansible Visual API funcionando"}


@app.get("/health")
def health():
    return {"status": "ok"}
