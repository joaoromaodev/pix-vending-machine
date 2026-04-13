from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from decimal import Decimal, ROUND_HALF_UP
import mercadopago
import json
from app.core.config import settings
from app.core.database import get_connection

router = APIRouter()
sdk = mercadopago.SDK(settings.mp_token)


class ItemCarrinho(BaseModel):
    id: str
    name: str
    price: float
    qty: int


class PagamentoRequest(BaseModel):
    itens: list[ItemCarrinho]


@router.post("/gerar-pagamento")
async def gerar_pagamento(body: PagamentoRequest):
    if not body.itens:
        raise HTTPException(status_code=400, detail="Carrinho vazio.")

    total = sum(Decimal(str(item.price)) * item.qty for item in body.itens)
    total = float(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    descricao = ", ".join(f"{item.name} x{item.qty}" for item in body.itens)

    payment_data = {
        "transaction_amount": total,
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {"email": "cliente@cherrybomb.com"}
    }

    result = sdk.payment().create(payment_data)
    payment = result["response"]

    if "id" not in payment:
        raise HTTPException(status_code=400, detail="Erro ao gerar pagamento no Mercado Pago.")

    p_id = str(payment["id"])

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pagamentos (id, status, itens, total) VALUES (%s, %s, %s, %s)",
        (p_id, "pending", json.dumps([i.dict() for i in body.itens]), total)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "id": p_id,
        "total": total,
        "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
        "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
    }


@router.get("/status/{payment_id}")
async def verificar_status(payment_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM pagamentos WHERE id = %s", (payment_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return {"status": "not_found"}
    return {"status": row["status"]}


def aprovar_pagamento(p_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE pagamentos SET status = 'approved' WHERE id = %s", (p_id,))

    cursor.execute("SELECT itens FROM pagamentos WHERE id = %s", (p_id,))
    row = cursor.fetchone()

    if row:
        itens = json.loads(row["itens"])
        for item in itens:
            cursor.execute(
                "UPDATE produtos SET stock = GREATEST(0, stock - %s) WHERE id = %s",
                (item["qty"], item["id"])
            )

    conn.commit()
    cursor.close()
    conn.close()