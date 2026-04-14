import streamlit as st
import math

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
# SHOPEE
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
if valor_input:
    try:
        valor = float(valor_input.replace(",", "."))

        custo_fixo = MOTOBOY + CARTAO + caixa

        # =====================
        # DEFINIR ALVO
        # =====================
        if modo == "Receber valor líquido":
            alvo = valor
        else:
            custo = valor
            alvo = custo * 2 + custo_fixo  # custo + lucro + fixos

        # =====================
        # SHOPEE
        # =====================
        preco_shopee = math.ceil(alvo / 0.8)

        while True:
            taxas = taxa_shopee(preco_shopee)
            imposto = preco_shopee * IMPOSTO

            recebido = preco_shopee - taxas - imposto

            if modo == "Receber valor líquido":
                condicao = recebido >= alvo
            else:
                lucro = recebido - custo_fixo - custo
                condicao = lucro >= custo - 1

            if condicao:
                break

            preco_shopee += 1

        # =====================
        # AMAZON
        # =====================
        preco_amazon = math.ceil(alvo / 0.85)

        while True:
            recebido = preco_amazon * (1 - AMAZON_COMISSAO)

            if modo == "Receber valor líquido":
                condicao = recebido >= alvo
            else:
                lucro = recebido - custo_fixo - custo
                condicao = lucro >= custo - 1

            if condicao:
                break

            preco_amazon += 1

        # =====================
        # MERCADO LIVRE
        # =====================
        if taxa_ml_input:
            taxa_ml = float(taxa_ml_input.replace(",", ".")) / 100

            preco_ml = math.ceil(alvo / (1 - taxa_ml))

            while True:
                recebido = preco_ml * (1 - taxa_ml)

                if modo == "Receber valor líquido":
                    condicao = recebido >= alvo
                else:
                    lucro = recebido - custo_fixo - custo
                    condicao = lucro >= custo - 1

                if condicao:
                    break

                preco_ml += 1
        else:
            preco_ml = None

        # =====================
        # RESULTADOS
        # =====================
        st.subheader("📊 Resultados")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🟧 Shopee")
            st.success(f"R$ {preco_shopee:.2f}")

        with col2:
            st.markdown("### 🟦 Amazon")
            st.success(f"R$ {preco_amazon:.2f}")

        with col3:
            st.markdown("### 🟨 Mercado Livre")
            if preco_ml:
                st.success(f"R$ {preco_ml:.2f}")
            else:
                st.warning("Informe a taxa")

    except:
        st.error("Digite valores válidos")
