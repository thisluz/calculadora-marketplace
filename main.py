import streamlit as st
import math

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Calculadora Marketplace", page_icon="🧮")

st.title("🧮 Calculadora de Preço")
st.caption("Amazon e Shopee: cálculo baseado em valor mínimo desejado")

# =====================
# AMAZON
# =====================
st.subheader("🟦 Amazon")

AMAZON_COMISSAO = 0.15  # FIXO
st.write("Comissão fixa Amazon: 15%")

valor_minimo_amazon = st.text_input(
    "Valor mínimo que você deseja receber (R$)",
    placeholder="Ex: 50,00",
    key="amazon_min"
)

frete_amazon = st.text_input(
    "Frete (R$)",
    placeholder="Ex: 10,00",
    key="amazon_frete"
)

if valor_minimo_amazon and frete_amazon:
    try:
        valor_minimo_amazon = float(valor_minimo_amazon.replace(",", "."))
        frete_amazon = float(frete_amazon.replace(",", "."))

        preco_venda = math.ceil(
            (valor_minimo_amazon + frete_amazon) / (1 - AMAZON_COMISSAO) - frete_amazon
        )

        while True:
            valor_recebido = (preco_venda + frete_amazon) * (1 - AMAZON_COMISSAO) - frete_amazon

            if valor_recebido >= valor_minimo_amazon:
                break

            preco_venda += 1

        st.success(f"💰 Preço mínimo de venda: R$ {preco_venda:.2f}")
        st.info(f"📥 Valor recebido: R$ {valor_recebido:.2f}")

    except ValueError:
        st.error("Digite apenas números válidos (use vírgula ou ponto).")

with st.expander("📐 Fórmula utilizada (Amazon)"):
    st.markdown("""
A Amazon cobra 15% sobre (preço + frete).

Fórmula base:
valor_recebido = (preço + frete) × (1 - 0,15) - frete

O sistema ajusta o preço até garantir:
valor_recebido ≥ valor mínimo desejado
""")

# =====================
# SHOPEE
# =====================
st.subheader("🟧 Shopee")

valor_minimo_shopee = st.text_input(
    "Valor mínimo que você deseja receber (R$)",
    placeholder="Ex: 50,00",
    key="shopee_min"
)

def calcular_taxas_shopee(preco):
    if preco <= 79.99:
        comissao = preco * 0.20
        taxa_fixa = 4
    elif preco <= 99.99:
        comissao = preco * 0.14
        taxa_fixa = 16
    elif preco <= 199.99:
        comissao = preco * 0.14
        taxa_fixa = 20
    else:
        comissao = preco * 0.14
        taxa_fixa = 26

    return comissao + taxa_fixa

if valor_minimo_shopee:
    try:
        valor_minimo_shopee = float(valor_minimo_shopee.replace(",", "."))

        preco_venda = math.ceil(valor_minimo_shopee / (1 - 0.20))  # estimativa inicial

        while True:
            taxas = calcular_taxas_shopee(preco_venda)
            valor_recebido = preco_venda - taxas

            if valor_recebido >= valor_minimo_shopee:
                break

            preco_venda += 1

        st.success(f"💰 Preço mínimo de venda: R$ {preco_venda:.2f}")
        st.info(f"📥 Valor recebido: R$ {valor_recebido:.2f}")

    except ValueError:
        st.error("Digite apenas números válidos (use vírgula ou ponto).")

with st.expander("📐 Fórmula utilizada (Shopee)"):
    st.markdown("""
Regras Shopee (2026):

- Até R$79,99 → 20% + R$4  
- R$80 a R$99,99 → 14% + R$16  
- R$100 a R$199,99 → 14% + R$20  
- Acima de R$200 → 14% + R$26  

Cálculo:

1. Define a faixa pelo preço  
2. Calcula comissão + taxa fixa  
3. Subtrai do preço  
4. Ajusta o preço até garantir:

valor_recebido ≥ valor mínimo
""")
