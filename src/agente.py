from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def percentual(valor: float) -> str:
    return f"{valor:.1f}%".replace(".", ",")


@dataclass
class ContextoFinanceiro:
    perfil: dict[str, Any]
    produtos: list[dict[str, Any]]
    transacoes: list[dict[str, Any]]
    atendimentos: list[dict[str, Any]]

    @property
    def entradas(self) -> float:
        return sum(t["valor"] for t in self.transacoes if t["tipo"] == "entrada")

    @property
    def saidas(self) -> float:
        return sum(t["valor"] for t in self.transacoes if t["tipo"] == "saida")

    @property
    def saldo_periodo(self) -> float:
        return self.entradas - self.saidas

    @property
    def gastos_por_categoria(self) -> dict[str, float]:
        totais: dict[str, float] = defaultdict(float)
        for transacao in self.transacoes:
            if transacao["tipo"] == "saida":
                totais[transacao["categoria"]] += transacao["valor"]
        return dict(sorted(totais.items(), key=lambda item: item[1], reverse=True))

    @property
    def meta_reserva(self) -> dict[str, Any] | None:
        for meta in self.perfil.get("metas", []):
            if "reserva" in meta.get("meta", "").lower():
                return meta
        return None

    @property
    def progresso_reserva(self) -> tuple[float, float, float]:
        meta = self.meta_reserva or {}
        atual = float(self.perfil.get("reserva_emergencia_atual", 0))
        alvo = float(meta.get("valor_necessario", 0))
        progresso = (atual / alvo * 100) if alvo else 0
        return atual, alvo, progresso if progresso <= 100 else 100

    @property
    def produtos_adequados_reserva(self) -> list[dict[str, Any]]:
        return [
            produto
            for produto in self.produtos
            if produto.get("risco") == "baixo"
            and (
                "liquidez" in produto.get("nome", "").lower()
                or "reserva" in produto.get("indicado_para", "").lower()
                or "liquidez" in produto.get("indicado_para", "").lower()
            )
        ]


def carregar_contexto() -> ContextoFinanceiro:
    with (DATA_DIR / "perfil_investidor.json").open(encoding="utf-8") as arquivo:
        perfil = json.load(arquivo)

    with (DATA_DIR / "produtos_financeiros.json").open(encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)

    transacoes = _ler_csv(DATA_DIR / "transacoes.csv")
    for transacao in transacoes:
        transacao["valor"] = float(transacao["valor"])

    atendimentos = _ler_csv(DATA_DIR / "historico_atendimento.csv")
    return ContextoFinanceiro(perfil, produtos, transacoes, atendimentos)


def _ler_csv(caminho: Path) -> list[dict[str, Any]]:
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


class BiaFuturo:
    def __init__(self, contexto: ContextoFinanceiro | None = None) -> None:
        self.contexto = contexto or carregar_contexto()

    def responder(self, pergunta: str) -> str:
        texto = pergunta.lower().strip()

        if self._pedido_sensivel(texto):
            return (
                "Nao posso acessar ou compartilhar senhas, credenciais, dados sensiveis "
                "ou informacoes de outros clientes. Posso ajudar com orientacoes financeiras "
                "usando apenas os dados mockados deste projeto."
            )

        if self._fora_do_escopo(texto):
            return (
                "Sou especializada em financas pessoais e nao tenho dados para responder "
                "sobre esse tema. Posso te ajudar a analisar gastos, metas, reserva de "
                "emergencia ou produtos financeiros cadastrados."
            )

        if any(palavra in texto for palavra in ["reserva", "meta", "emergência", "emergencia"]):
            return self._resposta_reserva()

        if any(palavra in texto for palavra in ["gasto", "gastei", "despesa", "categoria", "onde"]):
            return self._resposta_gastos()

        if any(palavra in texto for palavra in ["invest", "produto", "cdb", "tesouro", "selic", "recomenda"]):
            return self._resposta_produtos(texto)

        if any(palavra in texto for palavra in ["saldo", "receita", "entrada", "saída", "saida"]):
            return self._resposta_saldo()

        return self._resposta_geral()

    def _resposta_reserva(self) -> str:
        atual, alvo, progresso = self.contexto.progresso_reserva
        faltante = max(alvo - atual, 0)
        produtos = ", ".join(p["nome"] for p in self.contexto.produtos_adequados_reserva)

        return (
            f"{self.contexto.perfil['nome']}, sua reserva de emergencia esta em "
            f"{moeda(atual)} de uma meta de {moeda(alvo)}. Isso representa "
            f"{percentual(progresso)} do objetivo, entao faltam {moeda(faltante)} para completar a meta. "
            f"Como seu objetivo principal e {self.contexto.perfil['objetivo_principal'].lower()} "
            f"e voce nao aceita risco elevado, eu priorizaria opcoes de baixo risco e liquidez, "
            f"como {produtos}. Proximo passo: separar um aporte mensal fixo ate completar a reserva."
        )

    def _resposta_gastos(self) -> str:
        categorias = self.contexto.gastos_por_categoria
        linhas = [f"{categoria}: {moeda(valor)}" for categoria, valor in categorias.items()]
        maior_categoria, maior_valor = next(iter(categorias.items()))

        return (
            f"No periodo analisado, suas saidas somam {moeda(self.contexto.saidas)}. "
            f"A maior categoria e {maior_categoria}, com {moeda(maior_valor)}. "
            f"Resumo por categoria: {'; '.join(linhas)}. "
            "Proximo passo: revisar primeiro as despesas variaveis antes de alterar custos essenciais."
        )

    def _resposta_produtos(self, texto: str) -> str:
        nomes_produtos = {produto["nome"].lower(): produto for produto in self.contexto.produtos}
        for nome, produto in nomes_produtos.items():
            if nome in texto:
                return (
                    f"O produto {produto['nome']} esta cadastrado como {produto['categoria']}, "
                    f"risco {produto['risco']}, rentabilidade {produto['rentabilidade']} e aporte "
                    f"minimo de {moeda(float(produto['aporte_minimo']))}. Indicacao da base: "
                    f"{produto['indicado_para']}. Antes de contratar, confirme prazo, liquidez e "
                    "adequacao ao seu objetivo."
                )

        produtos = self.contexto.produtos_adequados_reserva
        detalhes = [
            f"{p['nome']} ({p['risco']}, {p['rentabilidade']}, aporte minimo {moeda(float(p['aporte_minimo']))})"
            for p in produtos
        ]
        return (
            "Para seu objetivo atual de reserva de emergencia, as opcoes mais coerentes na base sao "
            f"{'; '.join(detalhes)}. Evitei sugerir produtos de risco alto porque o cadastro informa "
            "que voce nao aceita risco elevado para esse momento."
        )

    def _resposta_saldo(self) -> str:
        return (
            f"No periodo analisado, voce teve {moeda(self.contexto.entradas)} em entradas e "
            f"{moeda(self.contexto.saidas)} em saidas. O saldo do periodo foi "
            f"{moeda(self.contexto.saldo_periodo)}. Proximo passo: direcionar parte desse saldo "
            "para completar a reserva de emergencia."
        )

    def _resposta_geral(self) -> str:
        perfil = self.contexto.perfil
        return (
            f"Ola, {perfil['nome']}! Posso te ajudar com sua reserva de emergencia, analise de gastos, "
            "saldo do periodo ou comparacao de produtos financeiros cadastrados. Com os dados atuais, "
            f"seu foco principal e {perfil['objetivo_principal'].lower()}."
        )

    @staticmethod
    def _pedido_sensivel(texto: str) -> bool:
        termos = ["senha", "token", "cpf", "pix de outro", "dados de outro", "cliente x"]
        return any(termo in texto for termo in termos)

    @staticmethod
    def _fora_do_escopo(texto: str) -> bool:
        termos = ["previsão do tempo", "previsao do tempo", "receita de bolo", "futebol", "filme"]
        return any(termo in texto for termo in termos)


if __name__ == "__main__":
    agente = BiaFuturo()
    print(agente.responder("Como esta minha reserva de emergencia?"))
