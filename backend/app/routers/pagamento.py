from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mercadopago
from app.core.config import settings

router = APIRouter()
sdk = mercadopago.SDK(settings.mp_token)

# Banco temporário em memória (Fase 2 — vira SQLite na Fase 4)
db_pagamentos = {}


# ─────────────────────────────────────────
# MODELOS
# ─────────────────────────────────────────
class ItemCarrinho(BaseModel):
    id: str        # ex: "A1"
    name: str      # ex: "Colar"
    price: float   # ex: 15.00
    qty: int       # ex: 2


class PagamentoRequest(BaseModel):
    itens: list[ItemCarrinho]


# ─────────────────────────────────────────
# POST /gerar-pagamento
# ─────────────────────────────────────────
@router.post("/gerar-pagamento")
async def gerar_pagamento(body: PagamentoRequest):
    if not body.itens:
        raise HTTPException(status_code=400, detail="Carrinho vazio.")

    # Calcula total real
    total = sum(item.price * item.qty for item in body.itens)
    total = round(total, 2)

    # Descrição dinâmica (ex: "Colar x2, Pulseira x1")
    descricao = ", ".join(
        f"{item.name} x{item.qty}" for item in body.itens
    )

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
    db_pagamentos[p_id] = "pending"

    return {
        "id": p_id,
        "total": total,
        "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
        "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
    }


# ─────────────────────────────────────────
# GET /status/{payment_id}
# ─────────────────────────────────────────
@router.get("/status/{payment_id}")
async def verificar_status(payment_id: str):
    return {"status": db_pagamentos.get(payment_id, "not_found")}