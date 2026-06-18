# Codigo da Aplicacao

Esta pasta contem o codigo da **BIA Futuro**, um agente financeiro generativo criado para o bootcamp Bradesco/DIO.

## Estrutura

```text
src/
├── app.py              # Interface principal em Streamlit
├── agente.py           # Logica do agente e integracao com a base de conhecimento
└── requirements.txt    # Dependencias da aplicacao
```

## Como Rodar

Instale as dependencias:

```bash
pip install -r src/requirements.txt
```

Execute a aplicacao:

```bash
streamlit run src/app.py
```

Tambem e possivel testar a logica do agente sem interface:

```bash
python src/agente.py
```
