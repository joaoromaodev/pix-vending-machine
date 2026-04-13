from fastapi import APIRouter, HTTPException, Header, UploadFile, File
from pydantic import BaseModel
from app.core.database import get_connection
import cloudinary
import cloudinary.uploader
import os

router = APIRouter(prefix="/admin")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "cherrybomb123")


def verificar_senha(x_admin_password: str = Header(...)):
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Senha incorreta.")


class ProdutoUpdate(BaseModel):
    name: str
    price: float
    stock: int
    image_url: str | None = None


@router.get("/produtos")
def admin_listar_produtos(x_admin_password: str = Header(...)):
    verificar_senha(x_admin_password)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, stock, image_url FROM produtos ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in rows]


@router.put("/produtos/{produto_id}")
def admin_atualizar_produto(
    produto_id: str,
    body: ProdutoUpdate,
    x_admin_password: str = Header(...)
):
    verificar_senha(x_admin_password)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produtos SET name=%s, price=%s, stock=%s, image_url=%s WHERE id=%s",
        (body.name, body.price, body.stock, body.image_url, produto_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "ok", "id": produto_id}


@router.post("/upload/{produto_id}")
async def admin_upload_imagem(
    produto_id: str,
    file: UploadFile = File(...),
    x_admin_password: str = Header(...)
):
    verificar_senha(x_admin_password)

    contents = await file.read()
    result = cloudinary.uploader.upload(
        contents,
        public_id=f"cherry_bomb/{produto_id}",
        overwrite=True,
        transformation=[
            {"width": 400, "height": 400, "crop": "fill", "gravity": "auto"}
        ]
    )

    image_url = result["secure_url"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produtos SET image_url=%s WHERE id=%s",
        (image_url, produto_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "ok", "image_url": image_url}