import streamlit as st
import math

st.set_page_config(page_title="Calculadora Amazon & Shopee", layout="centered")

st.title("📦 Calculadora de Preço de Venda")
st.caption("Calcule o preço mínimo de venda para Amazon e Shopee garantindo o valor líquido desejado.")

st.divider()

# =====================
# AMAZON
# =====================
st.subheader("🟠 Amazon")

AMAZON_COMISSAO = 0.15  # fixa

valor_minimo_amazon = st.text_input(
    "Valor mínimo que você deseja receber (R$)",
    placeholder="Ex: 50,00"
)

frete_amazon = st.text_input(
    "Frete (R$)",
    placeholder="Ex: 12,90"
)

st.caption("Comissão Amazon: 15% (fixa)")

if valor_minimo_amazon and frete_amazon:
    try:
        valor_minimo_amazon = float(valor_minimo_amazon.replace(",", "."))
        frete_amazon = float(frete_amazon.replace(",", "."))

        preco_venda_amazon = math.ceil(
            (valor_minimo_amazon + frete_amazon) / (1 - AMAZON_COMISSAO) - frete_amazon
        )

        valor_recebido_amazon = (
            (preco_venda_amazon + frete_amazon) * (1 - AMAZON_COMISSAO) - frete_amazon
        )

        st.success(f"💰 Preço mínimo de venda: R$ {preco_venda_amazon:.2f}")
        st.info(f"📥 Valor recebido: R$ {valor_recebido_amazon:.2f}")

    except ValueError:
        st.error("Digite apenas números válidos (use vírgula ou ponto).")

with st.expander("📐 Fórmula utilizada (Amazon)"):
    st.markdown("""
**Recebido:**  
(recebido) = (preço_venda + frete) × (1 − 0,15) − frete  

**Preço mínimo de venda:**  
preço_venda = ceil((valor_mínimo + frete) ÷ (1 − 0,15) − frete)
""")

st.divider()

# =====================
# SHOPEE
# =====================
st.subheader("🟧 Shopee")

SHOPEE_COMISSAO = 0.14
SHOPEE_TETO_COMISSAO = 104.00
SHOPEE_TAXA_FIXA = 4.00

valor_minimo_shopee = st.text_input(
    "Valor mínimo que você deseja receber (R$)",
    placeholder="Ex: 50,00",
    key="shopee_min"
)

if valor_minimo_shopee:
    try:
        valor_minimo_shopee = float(valor_minimo_shopee.replace(",", "."))

        preco_estimado = valor_minimo_shopee / (1 - SHOPEE_COMISSAO)
        comissao_calculada = preco_estimado * SHOPEE_COMISSAO
        comissao_final = min(comissao_calculada, SHOPEE_TETO_COMISSAO)

        preco_venda_shopee = math.ceil(
            valor_minimo_shopee + comissao_final + SHOPEE_TAXA_FIXA
        )

        valor_recebido_shopee = (
            preco_venda_shopee
            - min(preco_venda_shopee * SHOPEE_COMISSAO, SHOPEE_TETO_COMISSAO)
            - SHOPEE_TAXA_FIXA
        )

        st.success(f"💰 Preço mínimo de venda: R$ {preco_venda_shopee:.2f}")
        st.info(f"📥 Valor recebido: R$ {valor_recebido_shopee:.2f}")

    except ValueError:
        st.error("Digite apenas números válidos (use vírgula ou ponto).")

with st.expander("📐 Fórmula utilizada (Shopee)"):
    st.markdown("""
**Regras Shopee:**
- Comissão: 14% apenas sobre o valor do produto
- Comissão máxima: R$ 104,00
- Taxa fixa: R$ 4,00 por item

**Preço mínimo de venda:**  
preço_venda = valor_mínimo + comissão + taxa_fixa  

onde:  
comissão = min(preço_venda × 0,14, 104)
""")

st.divider()

st.caption("Calculadora pensada para uso real em marketplaces brasileiros.")
