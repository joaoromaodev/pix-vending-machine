from fastapi import APIRouter, HTTPException
from app.core.database import get_connection

router = APIRouter()


@router.get("/produtos")
def listar_produtos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, stock, image_url FROM produtos ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/produtos/{produto_id}")
def get_produto(produto_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, stock, image_url FROM produtos WHERE id = %s", (produto_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return dict(row)