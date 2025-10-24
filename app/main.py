from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.social.routes import router as social_router
from app.modules.analysis.routes import router as analysis_router
from app.config import settings

app = FastAPI(
    title="Social AI Backend",
    description="Backend modular en FastAPI para recolección y análisis de publicaciones en redes sociales.",
    version="0.1.0"
)

origins = [
    "http://localhost:8000",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "El backend de SentiData esta funcionando correctamente.",
        "version": "2.1.0"
    }

# ==========================================================
# Registrar routers de módulos (se agregarán progresivamente)
# ==========================================================
# app.include_router(social_router, prefix="/social", tags=["Social"])
# app.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
# app.include_router(gsheet_router, prefix="/gsheet", tags=["Google Sheets"])
app.include_router(social_router, prefix="/social", tags=["Social"])
app.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
