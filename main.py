import streamlit as st
import math

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Calculadora Marketplace", page_icon="🧮")

st.title("🧮 Calculadora de Preço")
st.caption("Baseado em lucro desejado (lucro = custo do produto)")

# =====================
# INPUTS
# =====================
custo_produto = st.text_input(
    "Custo do produto (R$)",
    placeholder="Ex: 16,50"
)

embalagem = st.selectbox(
    "Embalagem",
    ["Caixa pequena (0,93)", "Caixa grande (1,65)"]
)

st.subheader("🟨 Mercado Livre (baseado no simulador)")

preco_teste_ml = st.text_input(
    "Preço testado no ML (R$)",
    placeholder="Ex: 57"
)

recebido_ml = st.text_input(
    "Quanto você recebe no simulador (R$)",
    placeholder="Ex: 38,80"
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
if custo_produto:
    try:
        custo = float(custo_produto.replace(",", "."))

        custo_fixo = MOTOBOY + CARTAO + caixa
        lucro_desejado = custo

        # =====================
        # SHOPEE
        # =====================
        preco_shopee = math.ceil((custo + custo_fixo) / 0.8)

        while True:
            taxas = taxa_shopee(preco_shopee)
            imposto = preco_shopee * IMPOSTO

            lucro_shopee = preco_shopee - taxas - imposto - custo_fixo - custo

            if lucro_shopee >= lucro_desejado - 1:
                break

            preco_shopee += 1

        # =====================
        # AMAZON
        # =====================
        preco_amazon = math.ceil((custo + custo_fixo + lucro_desejado) / 0.85)

        while True:
            recebido = preco_amazon * (1 - AMAZON_COMISSAO)
            lucro_amazon = recebido - custo_fixo - custo

            if lucro_amazon >= lucro_desejado - 1:
                break

            preco_amazon += 1

        # =====================
        # MERCADO LIVRE (REAL)
        # =====================
        if preco_teste_ml and recebido_ml:
            preco_teste = float(preco_teste_ml.replace(",", "."))
            recebido_teste = float(recebido_ml.replace(",", "."))

            taxa_real_ml = 1 - (recebido_teste / preco_teste)

            preco_ml = math.ceil((custo + lucro_desejado + custo_fixo) / (1 - taxa_real_ml))

            while True:
                recebido_real = preco_ml * (1 - taxa_real_ml)
                lucro_ml = recebido_real - custo_fixo - custo

                if lucro_ml >= lucro_desejado - 1:
                    break

                preco_ml += 1
        else:
            preco_ml = None
            lucro_ml = None
            taxa_real_ml = None

        # =====================
        # RESULTADOS
        # =====================
        st.subheader("📊 Resultados")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🟧 Shopee")
            st.success(f"Preço: R$ {preco_shopee:.2f}")
            st.info(f"Lucro: R$ {lucro_shopee:.2f}")

        with col2:
            st.markdown("### 🟦 Amazon")
            st.success(f"Preço: R$ {preco_amazon:.2f}")
            st.info(f"Lucro: R$ {lucro_amazon:.2f}")

        with col3:
            st.markdown("### 🟨 Mercado Livre")
            if preco_ml:
                st.success(f"Preço: R$ {preco_ml:.2f}")
                st.info(f"Lucro: R$ {lucro_ml:.2f}")
                st.caption(f"Taxa real usada: {taxa_real_ml*100:.1f}%")
            else:
                st.warning("Preencha os dados do simulador")

    except:
        st.error("Digite valores válidos (use vírgula ou ponto).")

# =====================
# EXPLICAÇÃO
# =====================
with st.expander("📐 Como o cálculo funciona"):
    st.markdown("""
O objetivo é garantir:

lucro ≥ custo do produto

Mercado Livre usa taxa REAL baseada no simulador:

taxa_real = 1 - (recebido / preço)

Isso evita erros e reflete exatamente o que você recebe.
""")
