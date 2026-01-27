import streamlit as st
import math

st.set_page_config(page_title="Calculadora Amazon & Shopee")

st.title("📦 Calculadora de Preço de Venda")

marketplace = st.selectbox(
    "Marketplace",
    ["Amazon", "Shopee"]
)

st.divider()

valor_minimo = st.number_input(
    "Quanto você quer receber líquido (R$)",
    min_value=0.0,
    step=1.0
)

# ---------------- AMAZON ----------------
if marketplace == "Amazon":
    frete = st.number_input(
        "Frete (R$)",
        min_value=0.0,
        step=1.0
    )

    comissao = st.number_input(
        "Comissão (%)",
        min_value=0.0,
        max_value=100.0,
        value=15.0
    ) / 100

    if st.button("Calcular preço Amazon"):
        preco_venda = math.ceil(
            (valor_minimo + frete) / (1 - comissao) - frete
        )

        valor_recebido = (
            (preco_venda + frete) * (1 - comissao) - frete
        )

        st.success(f"Preço mínimo de venda: R$ {preco_venda:.2f}")
        st.caption(f"Você receberá: R$ {valor_recebido:.2f}")

# ---------------- SHOPEE ----------------
if marketplace == "Shopee":
    TAXA_PERCENTUAL = 0.14
    TAXA_FIXA = 4.0
    TETO_COMISSAO = 104.0

    if st.button("Calcular preço Shopee"):
        # Regime percentual
        preco_percentual = math.ceil(
            (valor_minimo + TAXA_FIXA) / (1 - TAXA_PERCENTUAL)
        )

        comissao_calculada = preco_percentual * TAXA_PERCENTUAL

        # Verifica teto
        if comissao_calculada > TETO_COMISSAO:
            preco_venda = math.ceil(valor_minimo + TAXA_FIXA + TETO_COMISSAO)
        else:
            preco_venda = preco_percentual

        # Conferência
        comissao_final = min(preco_venda * TAXA_PERCENTUAL, TETO_COMISSAO)
        valor_recebido = preco_venda - comissao_final - TAXA_FIXA

        st.success(f"Preço mínimo de venda: R$ {preco_venda:.2f}")
        st.caption(f"Você receberá: R$ {valor_recebido:.2f}")


