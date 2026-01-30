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

        # Estimativa inicial
        preco_venda = math.ceil(valor_minimo_shopee / (1 - SHOPEE_COMISSAO))

        # Ajuste iterativo para garantir valor mínimo real
        while True:
            comissao = min(preco_venda * SHOPEE_COMISSAO, SHOPEE_TETO_COMISSAO)
            valor_recebido = preco_venda - comissao - SHOPEE_TAXA_FIXA

            if valor_recebido >= valor_minimo_shopee:
                break

            preco_venda += 1

        st.success(f"💰 Preço mínimo de venda: R$ {preco_venda:.2f}")
        st.info(f"📥 Valor recebido: R$ {valor_recebido:.2f}")

    except ValueError:
        st.error("Digite apenas números válidos (use vírgula ou ponto).")

with st.expander("📐 Fórmula utilizada (Shopee)"):
    st.markdown("""
**Regras Shopee:**
- Comissão: 14% apenas sobre o valor do produto  
- Comissão máxima: R$ 104,00  
- Taxa fixa: R$ 4,00 por item  

**Cálculo real utilizado no app:**

1. Estimamos um preço inicial  
2. Calculamos a comissão real:  
   comissão = min(preço_venda × 0,14, 104)

3. Calculamos o valor recebido:  
   valor_recebido = preço_venda − comissão − 4

4. Se o valor recebido for menor que o mínimo desejado,  
   aumentamos o preço até garantir:

   valor_recebido ≥ valor_mínimo
""")
