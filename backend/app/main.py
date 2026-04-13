from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mercadopago
from app.core.config import settings
from app.core.database import init_db
from app.routers import produtos, pagamento, admin

app = FastAPI(title="Cherry Bomb Handmade — API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sdk = mercadopago.SDK(settings.mp_token)

app.include_router(produtos.router)
app.include_router(pagamento.router)
app.include_router(admin.router)


@app.on_event("startup")
def startup():
    init_db()
    print("🍒 Cherry Bomb API iniciada — banco SQLite pronto")


@app.get("/")
def read_root():
    return {"status": "Cherry Bomb API Online 🍒"}


@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    if payload.get("type") == "payment":
        p_id = str(payload["data"]["id"])

        payment_info = sdk.payment().get(p_id)
        status = payment_info["response"].get("status")

        print(f"📦 Pagamento {p_id} — status: {status}")

        if status == "approved":
            print(f"✅ Pagamento {p_id} APROVADO!")
            from app.routers.pagamento import aprovar_pagamento
            aprovar_pagamento(p_id)
        else:
            print(f"⏳ Pagamento {p_id} ainda não aprovado — status: {status}")

    return {"status": "ok"}