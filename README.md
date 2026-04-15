
<div align="center">

# 🍒 Cherry Bomb Handmade
### Vending Machine de Artesanatos com Pagamento via Pix

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Railway-blue.svg)](https://railway.app/)
[![GitHub Pages](https://img.shields.io/badge/Frontend-GitHub%20Pages-black.svg)](https://pages.github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Uma vending machine física de artesanatos instalada em condomínios.**
O cliente escaneia um QR Code, monta a sacola, paga via Pix e a máquina libera os produtos automaticamente.

[🛍️ Ver Demo](https://joaoromaodev.github.io/pix-vending-machine/) · [📋 Documentação Técnica](docs/DOCUMENTACAO_TECNICA.md) · [🐛 Reportar Bug](https://github.com/joaoromaodev/pix-vending-machine/issues)

</div>

---

## 📌 Sobre o Projeto

O **Cherry Bomb Handmade** é uma solução completa de hardware e software para venda de artesanatos sem atendente. A ideia nasceu da necessidade de vender produtos handmade em condomínios de forma autônoma, sem dinheiro físico e sem maquininha de cartão.

O cliente acessa a loja escaneando um QR Code colado no vidro da máquina, seleciona os produtos, paga um único Pix e a máquina gira as molas físicas correspondentes para liberar os itens.

```
Cliente escaneia QR Code
        ↓
Seleciona produtos na vitrine mobile
        ↓
Paga via Pix (Mercado Pago)
        ↓
Webhook confirma o pagamento
        ↓
ESP32 recebe sinal via MQTT
        ↓
Molas giram e produtos são liberados 🍒
```

---

## ✨ Funcionalidades

### ✅ Concluído
- Interface mobile-first com estética Y2K / Pop-Punk Neobrutalista
- Grade de produtos 4×5 (20 slots A1→E4) renderizada dinamicamente
- Carrinho dinâmico com controle de estoque em tempo real
- Geração de QR Code Pix via API do Mercado Pago
- Webhook de confirmação de pagamento
- Subtração automática de estoque após pagamento aprovado
- Painel administrativo com login, edição de produtos e upload de fotos
- Hospedagem de imagens via Cloudinary
- Backend em produção no Railway com PostgreSQL persistente
- Frontend hospedado no GitHub Pages

### 🔜 Em Desenvolvimento
- Integração MQTT com ESP32 (aguardando chegada do hardware)
- Sensor de queda de produto (fallback físico)
- Estorno automático em caso de falha mecânica

---

## 🛠️ Stack Tecnológico

| Camada | Tecnologia |
|--------|-----------|
| Backend | FastAPI (Python 3.11) |
| Banco de Dados | PostgreSQL (Railway) |
| Frontend | HTML5 + Tailwind CSS + Vanilla JS |
| Pagamentos | Mercado Pago (Pix) |
| Imagens | Cloudinary |
| Hospedagem Backend | Railway |
| Hospedagem Frontend | GitHub Pages |
| Hardware | ESP32 WROOM-32 + Motor TT DC + Driver TB6612FNG |
| Protocolo IoT | MQTT (em implementação) |

---

## 🌐 Links de Produção

| Ambiente | URL |
|----------|-----|
| 🛍️ Vitrine (Cliente) | https://joaoromaodev.github.io/pix-vending-machine/ |
| 🔧 Painel Admin | https://joaoromaodev.github.io/pix-vending-machine/admin.html |
| ⚙️ API Backend | https://hearty-tranquility-production.up.railway.app |
| 📖 Docs da API | https://hearty-tranquility-production.up.railway.app/docs |

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.11+
- Conta no Mercado Pago (para tokens de API)
- PostgreSQL ou SQLite para desenvolvimento

### Instalação

```bash
# Clone o repositório
git clone https://github.com/joaoromaodev/pix-vending-machine.git
cd pix-vending-machine

# Entre na pasta do backend
cd backend

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Rode o servidor
uvicorn app.main:app --reload
```

### Variáveis de Ambiente necessárias (`.env`)

```env
MP_ACCESS_TOKEN_PRODUCAO=seu_token_aqui
MP_ACCESS_TOKEN_TESTE=seu_token_teste_aqui
ADMIN_PASSWORD=sua_senha_aqui
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret
DATABASE_URL=sua_url_postgresql
```

---

## 📁 Estrutura do Projeto

```
pix-vending-machine/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py        # Configurações e variáveis de ambiente
│   │   │   └── database.py      # Conexão PostgreSQL e init do banco
│   │   ├── data/
│   │   │   └── products.json    # Seed inicial dos produtos
│   │   └── routers/
│   │       ├── admin.py         # Rotas do painel admin
│   │       ├── pagamento.py     # Geração de Pix e polling de status
│   │       └── produtos.py      # Listagem de produtos
│   │   └── main.py              # Entry point + webhook Mercado Pago
│   ├── requirements.txt
│   ├── Procfile                 # Configuração Railway
│   └── nixpacks.toml            # Build config Railway
├── docs/
│   ├── DOCUMENTACAO_TECNICA.md  # Documentação técnica completa
│   ├── HARDWARE_INTERFACE.md    # Protocolo MQTT ESP32
│   ├── IV_DESIGN.md             # Identidade visual e UI/UX
│   └── PRODUCT_SPEC.md          # Especificação do produto
├── frontend/
│   └── assets/
│       ├── index.html           # Vitrine do cliente
│       ├── admin.html           # Painel administrativo
│       ├── logo.svg             # Logo (fundo vermelho)
│       └── logo-red.svg         # Logo (fundo branco)
└── hardware/
    └── src/
        └── main.cpp             # Firmware ESP32 (em desenvolvimento)
```

---

## 📡 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/produtos` | Lista todos os produtos |
| POST | `/gerar-pagamento` | Gera Pix com itens do carrinho |
| GET | `/status/{id}` | Verifica status do pagamento |
| POST | `/webhook` | Recebe confirmação do Mercado Pago |
| GET | `/admin/produtos` | Lista produtos (admin) |
| PUT | `/admin/produtos/{id}` | Atualiza produto (admin) |
| POST | `/admin/upload/{id}` | Upload de foto para Cloudinary |

---

## 🎨 Identidade Visual

O projeto segue uma estética **Y2K / Pop-Punk Neobrutalista** inspirada em adesivos Polaroid.

| Cor | Hex | Uso |
|-----|-----|-----|
| Vermelho Cereja | `#C8102E` | Header, botões ADD, fundos de tela |
| Vermelho Escuro | `#8B0000` | Footer, botão sacola, ações destrutivas |
| Branco | `#FFFFFF` | Cards, fundos, textos sobre vermelho |
| Preto | `#1A1A1A` | Bordas, textos, badges |

**Tipografia:** Shrikhand (display) + Poppins (interface)

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Se você tem experiência com:

- **ESP32 / MQTT / Firmware** — a Fase 7 precisa de você!
- **Mecânica / Design Industrial** — carcaça e mecanismo de molas em planejamento
- **Frontend** — melhorias de UX são sempre bem-vindas

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👤 Autor

**João Romão**
📍 Belém, PA — Brasil
📧 romaocr33@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/joaoromao-data/)
🐙 [GitHub](https://github.com/joaoromaodev)

---

<div align="center">
Feito com ❤️ e muito ☕ em Belém do Pará
</div>
