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
# MERCADO LIVRE
# =====================
st.subheader("🟨 Mercado Livre")

ml_modo = st.radio(
    "Como calcular ML",
    ["Automático (valor recebido)", "Taxa estimada (%)", "Comissão + frete"]
)

recebido_ml_input = ""
taxa_ml_input = ""
comissao_ml_input = ""
frete_manual_input = ""
peso = None

if ml_modo == "Automático (valor recebido)":
    recebido_ml_input = st.text_input("Valor recebido", placeholder="Ex: 38,80")

elif ml_modo == "Taxa estimada (%)":
    taxa_ml_input = st.text_input("Taxa (%)", placeholder="Ex: 32")

elif ml_modo == "Comissão + frete":
    comissao_ml_input = st.text_input("Comissão (%)", placeholder="Ex: 16")

    peso = st.selectbox(
        "Peso do produto",
        [
            "Até 0,3 kg",
            "0,3 a 0,5 kg",
            "0,5 a 1 kg",
            "1 a 1,5 kg",
            "1,5 a 2 kg",
            "2 a 3 kg",
            "3 a 4 kg",
            "4 a 5 kg"
        ]
    )

    frete_manual_input = st.text_input(
        "Frete pago por você (quando grátis ≥79)",
        placeholder="Ex: 18"
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
# FRETE ML
# =====================
def frete_ml(peso, preco):
    tabela = {
        "Até 0,3 kg": [8.07, 9.36, 11.07, 24.70, 28.70, 32.90, 36.90, 41.90],
        "0,3 a 0,5 kg": [8.50, 9.50, 11.21, 26.50, 30.90, 35.30, 39.70, 45.10],
        "0,5 a 1 kg": [8.64, 9.64, 11.36, 27.70, 32.30, 36.90, 41.50, 47.30],
        "1 a 1,5 kg": [8.79, 9.79, 11.50, 28.30, 32.90, 37.70, 42.30, 49.30],
        "1,5 a 2 kg": [8.93, 9.93, 11.64, 28.90, 33.70, 38.50, 43.30, 49.30],
        "2 a 3 kg": [9.07, 11.36, 12.21, 31.50, 36.70, 42.10, 47.30, 52.50],
        "3 a 4 kg": [9.21, 11.64, 12.79, 34.10, 39.70, 45.30, 51.10, 56.70],
        "4 a 5 kg": [9.36, 11.93, 13.93, 36.90, 43.10, 49.30, 55.50, 61.50]
    }

    if preco <= 18.99:
        faixa = 0
    elif preco <= 48.99:
        faixa = 1
    elif preco <= 78.99:
        faixa = 2
    elif preco <= 99.99:
        faixa = 3
    elif preco <= 119.99:
        faixa = 4
    elif preco <= 149.99:
        faixa = 5
    elif preco <= 199.99:
        faixa = 6
    else:
        faixa = 7

    return tabela[peso][faixa]

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

        if modo == "Receber valor líquido":
            alvo = valor
        else:
            custo = valor
            lucro_desejado = custo
            alvo = custo + lucro_desejado + custo_fixo

        # SHOPEE
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

        # AMAZON
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

        # MERCADO LIVRE
        preco_ml = None

        if ml_modo == "Automático (valor recebido)" and recebido_ml_input:
            preco_teste = valor
            recebido_teste = float(recebido_ml_input.replace(",", "."))
            taxa_ml = 1 - (recebido_teste / preco_teste)

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

        elif ml_modo == "Taxa estimada (%)" and taxa_ml_input:
            taxa_ml = float(taxa_ml_input.replace(",", ".")) / 100

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

        elif ml_modo == "Comissão + frete" and comissao_ml_input and peso:
            comissao = float(comissao_ml_input.replace(",", ".")) / 100

            preco_ml = math.ceil(alvo / (1 - comissao))

            while True:
                frete_tabela = frete_ml(peso, preco_ml)

                if preco_ml >= 79:
                    if frete_manual_input:
                        frete = float(frete_manual_input.replace(",", "."))
                    else:
                        frete = frete_tabela
                else:
                    frete = frete_tabela

                recebido_ml = preco_ml * (1 - comissao) - frete

                if modo == "Receber valor líquido":
                    ok = recebido_ml >= alvo
                else:
                    lucro_ml = recebido_ml - custo_fixo - custo
                    ok = lucro_ml >= lucro_desejado - 1

                if ok:
                    break
                preco_ml += 1

        # OUTPUT
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
