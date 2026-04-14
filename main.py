import streamlit as st
import math

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Calculadora Marketplace", page_icon="🧮")

st.title("🧮 Calculadora de Preço")

# =====================
# MODO
# =====================
modo = st.radio(
    "Modo de cálculo",
    ["Receber valor líquido", "Lucro baseado no custo"]
)

# =====================
# INPUTS
# =====================
valor_input = st.text_input(
    "Valor base (R$)",
    placeholder="Ex: 16,50"
)

embalagem = st.selectbox(
    "Embalagem",
    ["Caixa pequena (0,93)", "Caixa grande (1,65)"]
)

taxa_ml_input = st.text_input(
    "Taxa Mercado Livre (%)",
    placeholder="Ex: 32"
)

# =====================
# CONSTANTES
# =====================
MOTOBOY = 4.80
CARTAO = 0.34
IMPOSTO = 0.06
AMAZON_COMISSAO = 0.15

caixa = 0.93 if "pequena" in embalagem else 1.65

# =====================
# FUNÇÃO SHOPEE
# =====================
def taxa_shopee(preco):
    if preco <= 79.99:
        return preco * 0.20 + 4
    elif preco <= 99.99:
        return preco * 0.14 + 16
    elif preco <= 199.99:
        return preco * 0.14 + 20
    else:
        return preco * 0.14 + 26

# =====================
# CALCULO
# =====================
if valor_input != "":
    try:
        valor = float(valor_input.replace(",", "."))
        custo_fixo = MOTOBOY + CARTAO + caixa

        # =====================
        # DEFINIÇÃO DO ALVO
        # =====================
        if modo == "Receber valor líquido":
            alvo = valor
        else:
            custo = valor
            alvo = custo * 2 + custo_fixo

        # =====================
        # SHOPEE
        # =====================
        preco_shopee = math.ceil(alvo / 0.8)

        while True:
            taxas = taxa_shopee(preco_shopee)
            imposto = preco_shopee * IMPOSTO
            recebido_shopee = preco_shopee - taxas - imposto

            if modo == "Receber valor líquido":
                ok = recebido_shopee >= alvo
            else:
                lucro_shopee = recebido_shopee - custo_fixo - custo
                ok = lucro_shopee >= custo - 1

            if ok:
                break

            preco_shopee += 1

        # =====================
        # AMAZON
        # =====================
        preco_amazon = math.ceil(alvo / 0.85)

        while True:
            recebido_amazon = preco_amazon * (1 - AMAZON_COMISSAO)

            if modo == "Receber valor líquido":
                ok = recebido_amazon >= alvo
            else:
                lucro_amazon = recebido_amazon - custo_fixo - custo
                ok = lucro_amazon >= custo - 1

            if ok:
                break

            preco_amazon += 1

        # =====================
        # MERCADO LIVRE
        # =====================
        preco_ml = None

        if taxa_ml_input != "":
            taxa_ml = float(taxa_ml_input.replace(",", ".")) / 100

            preco_ml = math.ceil(alvo / (1 - taxa_ml))

            while True:
                recebido_ml = preco_ml * (1 - taxa_ml)

                if modo == "Receber valor líquido":
                    ok = recebido_ml >= alvo
                else:
                    lucro_ml = recebido_ml - custo_fixo - custo
                    ok = lucro_ml >= custo - 1

                if ok:
                    break

                preco_ml += 1

        # =====================
        # OUTPUT
        # =====================
        st.subheader("📊 Resultados")

        col1, col2, col3 = st.columns(3)

        # SHOPEE
        with col1:
            st.markdown("### 🟧 Shopee")

            taxas = taxa_shopee(preco_shopee)
            imposto = preco_shopee * IMPOSTO
            recebido_shopee = preco_shopee - taxas - imposto

            st.success(f"Preço: R$ {preco_shopee:.2f}")

            if modo == "Receber valor líquido":
                st.info(f"Recebe: R$ {recebido_shopee:.2f}")
            else:
                lucro = recebido_shopee - custo_fixo - custo
                st.info(f"Lucro: R$ {lucro:.2f}")

        # AMAZON
        with col2:
            st.markdown("### 🟦 Amazon")

            recebido_amazon = preco_amazon * (1 - AMAZON_COMISSAO)

            st.success(f"Preço: R$ {preco_amazon:.2f}")

            if modo == "Receber valor líquido":
                st.info(f"Recebe: R$ {recebido_amazon:.2f}")
            else:
                lucro = recebido_amazon - custo_fixo - custo
                st.info(f"Lucro: R$ {lucro:.2f}")

        # MERCADO LIVRE
        with col3:
            st.markdown("### 🟨 Mercado Livre")

            if preco_ml:
                recebido_ml = preco_ml * (1 - taxa_ml)

                st.success(f"Preço: R$ {preco_ml:.2f}")

                if modo == "Receber valor líquido":
                    st.info(f"Recebe: R$ {recebido_ml:.2f}")
                else:
                    lucro = recebido_ml - custo_fixo - custo
                    st.info(f"Lucro: R$ {lucro:.2f}")
            else:
                st.warning("Informe a taxa")

    except Exception as e:
        st.error(f"Erro: {e}")

# =====================
# EXPLICAÇÃO
# =====================
with st.expander("📐 Como o cálculo funciona"):
    st.markdown("""
### Modo 1 — Receber valor líquido
Calcula o preço necessário para que, após taxas, você receba o valor informado.

### Modo 2 — Lucro baseado no custo
Garante que o lucro seja igual ao custo do produto.

### O cálculo considera:
- custo do produto  
- motoboy  
- embalagem  
- cartão  
- imposto (Shopee)  
- comissão de cada marketplace  
""")
