from __future__ import annotations

import streamlit as st

from agente import BiaFuturo, carregar_contexto, moeda


st.set_page_config(page_title="BIA Futuro", page_icon="BIA", layout="wide")


def markdown_seguro(texto: str) -> str:
    return texto.replace("$", r"\$")


@st.cache_resource
def obter_agente() -> BiaFuturo:
    return BiaFuturo(carregar_contexto())


agente = obter_agente()
contexto = agente.contexto
perfil = contexto.perfil
atual, alvo, progresso = contexto.progresso_reserva

st.title("BIA Futuro")
st.caption("Agente financeiro generativo para organizacao de gastos e reserva de emergencia")

coluna_reserva, coluna_saldo, coluna_perfil = st.columns(3)
coluna_reserva.metric("Reserva atual", moeda(atual), f"{progresso:.1f}% da meta".replace(".", ","))
coluna_saldo.metric("Saldo do periodo", moeda(contexto.saldo_periodo))
coluna_perfil.metric("Perfil", perfil["perfil_investidor"].title())

st.progress(min(progresso / 100, 1.0), text=f"Meta: {moeda(alvo)}")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": agente.responder("ola"),
        }
    ]

perguntas_rapidas = [
    "Como esta minha reserva de emergencia?",
    "Onde estou gastando mais?",
    "Qual produto combina com meu objetivo?",
    "Qual foi meu saldo no periodo?",
]

st.subheader("Chat")
colunas = st.columns(len(perguntas_rapidas))
for coluna, pergunta in zip(colunas, perguntas_rapidas):
    if coluna.button(pergunta, use_container_width=True):
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        st.session_state.mensagens.append({"role": "assistant", "content": agente.responder(pergunta)})

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(markdown_seguro(mensagem["content"]))

if pergunta := st.chat_input("Pergunte sobre gastos, metas, reserva ou produtos financeiros"):
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    resposta = agente.responder(pergunta)
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    st.rerun()

with st.sidebar:
    st.header("Base consultada")
    st.write(f"Cliente: {perfil['nome']}")
    st.write(f"Objetivo: {perfil['objetivo_principal']}")
    st.write(f"Renda mensal: {moeda(float(perfil['renda_mensal']))}")
    st.write("Produtos adequados para reserva:")
    for produto in contexto.produtos_adequados_reserva:
        st.write(f"- {produto['nome']} ({produto['rentabilidade']})")
