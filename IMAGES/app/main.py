from fastapi import FastAPI
from app.routers import images
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title="leo-images", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (em produção, especifique seus domínios)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
async def root():
    return {"status": "up"}
