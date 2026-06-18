# BIA Futuro - Agente Financeiro Inteligente com IA Generativa

## Contexto

A **BIA Futuro** e um prototipo de agente financeiro generativo criado para o bootcamp Bradesco/DIO. A proposta e evoluir assistentes virtuais financeiros de chatbots reativos para agentes consultivos, capazes de analisar contexto, orientar o cliente e reduzir riscos de respostas inventadas.

O agente foi construido com dados mockados e foco em:

- Antecipar necessidades financeiras.
- Personalizar respostas com base no perfil do cliente.
- Cocriar solucoes financeiras de forma educativa.
- Garantir seguranca e confiabilidade nas respostas.

---

## O Que Foi Entregue

### 1. Documentacao do Agente

Define caso de uso, persona, arquitetura, seguranca e limitacoes da BIA Futuro.

Arquivo: [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md)

### 2. Base de Conhecimento

Explica como os dados mockados da pasta `data/` sao usados para personalizar respostas.

Arquivo: [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md)

### 3. Prompts do Agente

Contem system prompt, exemplos de interacao e tratamento de casos sensiveis.

Arquivo: [`docs/03-prompts.md`](./docs/03-prompts.md)

### 4. Aplicacao Funcional

Protótipo em Streamlit com chat, perguntas rapidas e leitura da base local.

Arquivos principais:

- [`src/app.py`](./src/app.py)
- [`src/agente.py`](./src/agente.py)
- [`src/requirements.txt`](./src/requirements.txt)

### 5. Avaliacao e Metricas

Define testes de assertividade, seguranca, coerencia, utilidade e tom de voz.

Arquivo: [`docs/04-metricas.md`](./docs/04-metricas.md)

### 6. Pitch

Roteiro de apresentacao de ate 3 minutos para demonstrar o agente.

Arquivo: [`docs/05-pitch.md`](./docs/05-pitch.md)

### 7. Ciberseguranca

Plano inicial para protecao de dados, guardrails do agente, prompt injection, logs seguros e proximos passos com time de seguranca.

Arquivo: [`docs/06-ciberseguranca.md`](./docs/06-ciberseguranca.md)

---

## Como Rodar

Instale as dependencias:

```bash
pip install -r src/requirements.txt
```

Execute o app:

```bash
streamlit run src/app.py
```

Teste a logica do agente sem interface:

```bash
python src/agente.py
```

---

## Estrutura do Repositorio

```text
lab-agente-financeiro/
├── README.md
├── data/
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   ├── produtos_financeiros.json
│   └── transacoes.csv
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   ├── 05-pitch.md
│   └── 06-ciberseguranca.md
├── src/
│   ├── README.md
│   ├── agente.py
│   ├── app.py
│   └── requirements.txt
├── assets/
└── examples/
```

---

## Demonstracao Sugerida

Use estas perguntas no chat:

1. Como esta minha reserva de emergencia?
2. Onde estou gastando mais?
3. Qual produto combina com meu objetivo?
4. Me passa a senha do cliente X.

A quarta pergunta demonstra a recusa segura do agente diante de informacao sensivel.

---

## Observacao

Este projeto usa dados ficticios. A BIA Futuro nao realiza transacoes bancarias reais, nao substitui consultoria financeira regulada e nao promete rentabilidade.

##  Demonstração

Assista à demonstração completa da BIA Futuro AI:

[![Demo](https://img.shields.io/badge/▶%20Ver%20Demonstração-Drive-blue)](https://drive.google.com/file/d/1Qr77tl76h7yu61TcCKDcl85mwc7q7_ic/view?usp=sharing)
---

##  Tecnologias Utilizadas

- Python
- Streamlit
- CSV
- JSON
- IA baseada em regras
- Análise Financeira
