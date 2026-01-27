import streamlit as st
import math

st.set_page_config(page_title="Calculadora Amazon & Shopee")

st.title("📦 Calculadora de Preço de Venda")

marketplace = st.selectbox(
    "Marketplace",
    ["Amazon", "Shopee"]
)

st.divider()

def ler_numero(label, placeholder):
    texto = st.text_input(label, placeholder=placeholder)

    if texto.strip() == "":
        return None

    try:
        return float(texto.replace(",", "."))
    except ValueError:
        st.error(f"Digite apenas números no campo: {label}")
        return None

valor_minimo = ler_numero(
    "Quanto você quer receber líquido (R$)",
    "Ex: 120"
)

# ---------------- AMAZON ----------------
if marketplace == "Amazon":
    frete = ler_numero(
        "Frete (R$)",
        "Ex: 25"
    )

    comissao_txt = st.text_input(
        "Comissão (%)",
        placeholder="Ex: 15"
    )

    comissao = None
    if comissao_txt.strip() != "":
        try:
            comissao = float(comissao_txt.replace(",", ".")) / 100
        except ValueError:
            st.error("Digite apenas números no campo: Comissão (%)")

    if st.button("Calcular preço Amazon"):
        if None in (valor_minimo, frete, comissao):
            st.warning("Preencha todos os campos corretamente.")
        else:
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
        if valor_minimo is None:
            st.warning("Preencha o valor mínimo corretamente.")
        else:
            preco_percentual = math.ceil(
                (valor_minimo + TAXA_FIXA) / (1 - TAXA_PERCENTUAL)
            )

            comissao_calculada = preco_percentual * TAXA_PERCENTUAL

            if comissao_calculada > TETO_COMISSAO:
                preco_venda = math.ceil(valor_minimo + TAXA_FIXA + TETO_COMISSAO)
            else:
                preco_venda = preco_percentual

            comissao_final = min(preco_venda * TAXA_PERCENTUAL, TETO_COMISSAO)
            valor_recebido = preco_venda - comissao_final - TAXA_FIXA

            st.success(f"Preço mínimo de venda: R$ {preco_venda:.2f}")
            st.caption(f"Você receberá: R$ {valor_recebido:.2f}")
