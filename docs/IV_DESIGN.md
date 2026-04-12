# 🍒 Especificações de Identidade Visual e UI/UX (IV_DESIGN.md)

## 1. Visão Geral da Marca
* **Nome:** Cherry Bomb Handmade
* **Conceito:** Vending machine de artesanatos autênticos via QR Code e PIX.
* **Estética Core:** Y2K (anos 2000), Pop-Punk, Neobrutalismo focado em Polaroids.
* **Tom de Voz:** Direto, moderno e autêntico.
* **Abordagem UI:** Mobile-First absoluto (acesso exclusivo via QR code na máquina). Sem efeitos de "hover" ou "zoom", interface 100% estática e focada no toque.

---

## 2. Paleta de Cores (Bicolor Estrito)
A paleta abandona o rosa e foca no contraste absoluto entre o vermelho, o preto e o branco.

* **Cor Primária (Vermelho Cereja Vibrante):** `#C8102E` - Uso no header, fundo de modais de checkout e botões "ADD" padrão.
* **Cor Secundária (Vermelho Escuro):** `#8B0000` - Uso no rodapé (footer da sacola) e botão de lixeira ("X") para indicar uma ação destrutiva, criando profundidade sem sair da paleta.
* **Cor de Fundo/Cards:** `#FFFFFF` (Branco Puro) - Uso nas molduras de Polaroid e fundo da página.
* **Contraste e Linhas:** `#1A1A1A` (Preto Sólido) - Textos, preços e bordas neobrutalistas grossas.

---

## 3. Tipografia
* **Display (Títulos e Marcas):** `Shrikhand` ou `Bangers` (Uso no Header e telas de impacto).
* **Interface (Corpo e Botões):** `Poppins` ou `Outfit` (Fonte geométrica sem serifa, uso em nomes de produtos, botões e controles de quantidade).

---

## 4. Componentes de Interface (Polaroid Neobrutalista)
* **Estilo Geral:** Bordas sólidas pretas (`border-2 border-black`) em todos os cards e modais. Sem arredondamentos excessivos.
* **Cards de Produto (Mockup Polaroid):**
  * Fundo branco, formato vertical com a foto quadrada no topo.
  * Badge de identificação (Ex: A1, B4) colada no canto superior esquerdo da foto (Fundo preto, texto branco).
  * Informações em linha única abaixo da foto: `NOME - R$ XX,XX`.
* **Controles Dinâmicos (Botões):**
  * **Estado 1 (Vazio):** Botão "ADD" vermelho vibrante, largura total.
  * **Estado 2 (Selecionado):** Seletor embutido no formato `[ - ] [ Qtd ] [ + ] [ X ]`.
  * O botão `[ X ]` usa o Vermelho Escuro e serve para zerar a quantidade imediatamente.

---

## 5. Fluxo de Telas (Mobile)

### Tela 1: Vitrine (Home)
* **Header:** Fundo Vermelho Vibrante, Logo SVG centralizada com o texto "- HANDMADE -" em branco.
* **Body:** Grid de **4 colunas e 5 linhas (A1 a E4)**.
* **Sacola (Footer):** Barra fixa inferior com fundo branco, mostrando o "Subtotal R$ XX,XX" em vermelho à esquerda, e um ícone de sacola com fundo Vermelho Escuro à direita para ir ao Checkout.

### Tela 2: Pagamento (Checkout PIX)
* **Visual:** Fundo vermelho predominante.
* **Título:** "Quase lá! 🍒" (Fonte de Display branca).
* **Subtítulo:** "Finalize o pagamento via Pix para liberar seu pedido."
* **Elementos:** Card branco central com QR Code, botão "Copiar Código Pix" preto e indicador de "Aguardando confirmação...".

### Tela 3: Confirmação (Sucesso)
* **Gatilho:** Ativada automaticamente via polling de status (`approved`).
* **Visual:** Animação de sucesso (brilhos/cerejas).
* **Copywriting:** "Pagamento Aprovado! 🍒"
* **Instrução:** "Aguarde o giro das molas e retire seus mimos abaixo."

---

## 6. Lógica de Negócio (Frontend)
* Bloqueio automático de adição de itens caso exceda o estoque disponível.
* Ação do botão [X] deve retornar a quantidade para zero e restaurar o botão "ADD".
* Polling (consulta recorrente) ao backend a cada 3 segundos para detectar a aprovação do pagamento sem necessidade de atualização manual da página.