import streamlit as st
import math

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Calculadora Marketplace", page_icon="🧮")

st.title("🧮 Calculadora de Preço")

# =====================
# MODO GLOBAL
# =====================
modo = st.radio(
    "Modo de cálculo",
    ["Receber valor líquido", "Lucro baseado no custo"]
)

valor_input = st.text_input("Valor base (R$)", placeholder="Ex: 16,50")

embalagem = st.selectbox(
    "Embalagem",
    ["Caixa pequena (0,93)", "Caixa grande (1,65)"]
)

# =====================
# MERCADO LIVRE MODOS
# =====================
st.subheader("🟨 Mercado Livre")

ml_modo = st.radio(
    "Como calcular ML",
    ["Automático (valor recebido)", "Taxa estimada (%)", "Comissão + frete"]
)

recebido_ml_input = ""
taxa_ml_input = ""
frete_ml_input = ""
comissao_ml_input = ""

if ml_modo == "Automático (valor recebido)":
    recebido_ml_input = st.text_input("Valor recebido", placeholder="Ex: 38,80")

elif ml_modo == "Taxa estimada (%)":
    taxa_ml_input = st.text_input("Taxa (%)", placeholder="Ex: 32")

else:
    comissao_ml_input = st.text_input("Comissão (%)", placeholder="Ex: 16")
    frete_ml_input = st.text_input("Frete (R$)", placeholder="Ex: 10")

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

        if modo == "Receber valor líquido":
            alvo = valor
        else:
            custo = valor
            lucro_desejado = custo
            alvo = custo + lucro_desejado + custo_fixo

        # =====================
        # SHOPEE
        # =====================
        preco_shopee = math.ceil(alvo / 0.8)

        while True:
            taxas = taxa_shopee(preco_shopee)
            imposto = preco_shopee * IMPOSTO
            recebido = preco_shopee - taxas - imposto

            if modo == "Receber valor líquido":
                ok = recebido >= alvo
            else:
                lucro = recebido - custo_fixo - custo
                ok = lucro >= lucro_desejado - 1

            if ok:
                break

            preco_shopee += 1

        # =====================
        # AMAZON
        # =====================
        preco_amazon = math.ceil(alvo / 0.85)

        while True:
            recebido = preco_amazon * (1 - AMAZON_COMISSAO)

            if modo == "Receber valor líquido":
                ok = recebido >= alvo
            else:
                lucro = recebido - custo_fixo - custo
                ok = lucro >= lucro_desejado - 1

            if ok:
                break

            preco_amazon += 1

        # =====================
        # MERCADO LIVRE
        # =====================
        preco_ml = None
        taxa_ml = None

        # 🔹 MODO 1 - AUTOMÁTICO
        if ml_modo == "Automático (valor recebido)" and recebido_ml_input:
            preco_teste = valor
            recebido_teste = float(recebido_ml_input.replace(",", "."))
            taxa_ml = 1 - (recebido_teste / preco_teste)

        # 🔹 MODO 2 - TAXA
        elif ml_modo == "Taxa estimada (%)" and taxa_ml_input:
            taxa_ml = float(taxa_ml_input.replace(",", ".")) / 100

        # 🔹 MODO 3 - COMISSÃO + FRETE
        elif ml_modo == "Comissão + frete" and comissao_ml_input and frete_ml_input:
            comissao = float(comissao_ml_input.replace(",", ".")) / 100
            frete = float(frete_ml_input.replace(",", "."))

            preco_ml = math.ceil((alvo + frete) / (1 - comissao))

        # 🔁 LOOP (modos 1 e 2)
        if taxa_ml is not None:
            preco_ml = math.ceil(alvo / (1 - taxa_ml))

            while True:
                recebido_ml = preco_ml * (1 - taxa_ml)

                if modo == "Receber valor líquido":
                    ok = recebido_ml >= alvo
                else:
                    lucro_ml = recebido_ml - custo_fixo - custo
                    ok = lucro_ml >= lucro_desejado - 1

                if ok:
                    break

                preco_ml += 1

        # =====================
        # OUTPUT
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
                st.warning("Preencha os dados")

    except Exception as e:
        st.error(f"Erro: {e}")
