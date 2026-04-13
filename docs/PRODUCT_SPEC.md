# Especificação do Produto: Cherry Bomb Handmade

## Visão Geral
Uma máquina de vendas automática para artesanatos, operada via Pix, instalada em ambientes condominiais. O sistema elimina a necessidade de dinheiro físico ou maquininhas de cartão, utilizando apenas QR Codes e uma interface web mobile.

## Stack Tecnológico
- **Backend:** FastAPI (Python), PostgreSQL, deployado no Railway
- **Frontend:** HTML puro, Tailwind CSS via CDN, Vanilla JavaScript
- **Pagamentos:** Mercado Pago (Pix) via webhook
- **Imagens:** Cloudinary (upload e hospedagem permanente)
- **Hardware (futuro):** ESP32 via MQTT

## URLs de Produção
- **Backend:** https://hearty-tranquility-production.up.railway.app
- **Frontend:** https://romao666.github.io/pix-vending-machine
- **Admin:** frontend/assets/admin.html (aberto localmente por enquanto)

## Credenciais e Variáveis de Ambiente (Railway)
- `MP_ACCESS_TOKEN_PRODUCAO` — token Mercado Pago produção
- `MP_ACCESS_TOKEN_TESTE` — token Mercado Pago teste
- `ADMIN_PASSWORD` — senha do painel admin (`#CherryBomb6661`)
- `CLOUDINARY_CLOUD_NAME` — cloud name do Cloudinary
- `CLOUDINARY_API_KEY` — API key do Cloudinary
- `CLOUDINARY_API_SECRET` — API secret do Cloudinary
- `DATABASE_URL` — referência automática ao PostgreSQL do Railway

## Fluxo Principal (Happy Path)
1. **Acesso:** Cliente escaneia o QR Code físico na máquina (URL única).
2. **Seleção:** Cliente navega pelo grid 4×5 (A1→E4) de produtos.
3. **Carrinho:** Cliente adiciona itens e quantidades à sacola.
4. **Checkout:** Sistema gera um único Pix Copia e Cola (Mercado Pago).
5. **Confirmação:** Webhook recebe aprovação, subtrai estoque e dispara comando de hardware.
6. **Entrega:** A máquina gira as molas correspondentes sequencialmente.

## Gestão de Estoque
- Cada "mola" (coordenada A1→E4) tem um saldo de estoque no PostgreSQL.
- O sistema subtrai do banco **após** a confirmação do pagamento via webhook.
- Se um item chegar a zero, é desabilitado automaticamente na interface.

## Regras de Negócio
- **Sem Cadastro:** Foco em fricção zero.
- **Pagamento Multi-item:** Um único Pix pode acionar múltiplos motores.
- **Produto de teste:** E4 com valor R$ 0,01 para testes sem custo.

## Status do Desenvolvimento

### ✅ Concluído
- **Fase 1:** Frontend base — paleta, grid 4×5, carrinho funcional, bottom sheet, tela de pagamento, tela de sucesso com animação
- **Fase 2:** Backend sólido — products.json, GET /produtos, POST /gerar-pagamento com valor real, requirements.txt
- **Fase 3:** Integração frontend↔backend — cards dinâmicos, checkout real, QR Code real, polling de status
- **Fase 4:** Polimento + produção — animação de cerejas, deploy Railway, webhook Mercado Pago funcionando em produção
- **Fase 5:** Admin + Fotos — PostgreSQL persistente, Cloudinary, interface admin com login/edição/upload, fotos nos cards
- **Fase 6:** Estoque real — subtração após pagamento aprovado ✅

### 🔜 Próximo — Fase 7 e 8
- **Fase 7:** MQTT stub — disparo para ESP32 após pagamento aprovado
- **Fase 8:** Hospedagem do frontend (em andamento)

### 📋 Backlog
- Domínio personalizado configurado no Railway
- Proteção da rota /admin por URL secreta