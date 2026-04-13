from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()

DATA_PATH = Path(__file__).parent.parent / "data" / "products.json"

@router.get("/produtos")
def listar_produtos():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        produtos = json.load(f)
    return produtos