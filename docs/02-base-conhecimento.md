# Base de Conhecimento

## Dados Utilizados

Foram utilizados todos os arquivos mockados da pasta `data/`. Eles representam um cliente ficticio e permitem demonstrar personalizacao sem expor dados sensiveis reais.

| Arquivo | Formato | Utilizacao no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Identificar temas ja tratados, como CDB, Tesouro Selic e metas financeiras |
| `perfil_investidor.json` | JSON | Personalizar respostas com nome, renda, perfil, patrimonio, reserva atual e metas |
| `produtos_financeiros.json` | JSON | Filtrar produtos adequados ao objetivo e ao risco aceito pelo cliente |
| `transacoes.csv` | CSV | Calcular receitas, despesas, saldo do mes e gastos por categoria |

---

## Adaptacoes nos Dados

Os dados originais foram mantidos. A aplicacao cria indicadores derivados em tempo de execucao, como total de entradas, total de saidas, saldo mensal, gasto por categoria e progresso da reserva de emergencia.

---

## Estrategia de Integracao

### Como os dados sao carregados?

Os arquivos JSON e CSV sao carregados no inicio da sessao pelo modulo `src/agente.py`. O agente transforma esses dados em um resumo financeiro estruturado que pode ser exibido na interface e usado na geracao da resposta.

### Como os dados sao usados no prompt?

Os dados sao consultados dinamicamente a cada pergunta. O system prompt define comportamento, limites e regras de seguranca. O contexto do usuario contem os dados consolidados do cliente e somente os produtos disponiveis na base local.

---

## Exemplo de Contexto Montado

```text
Dados do Cliente:
- Nome: Joao Silva
- Perfil: moderado
- Renda mensal: R$ 5.000,00
- Objetivo principal: Construir reserva de emergencia
- Reserva atual: R$ 10.000,00
- Meta de reserva: R$ 15.000,00
- Progresso: 66,7%

Ultimas transacoes:
- 2026-06-02: Aluguel - R$ 1.200,00
- 2026-06-03: Supermercado - R$ 450,00
- 2026-06-10: Restaurante - R$ 120,00

Produtos compativeis com reserva:
- Tesouro Selic: risco baixo, 100% da Selic
- CDB Liquidez Diaria: risco baixo, 102% do CDI
```
