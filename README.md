# TrendsIA — Planejador de Rotina com LLM

> **Problema:** montar, pelo terminal, um plano de rotina para o dia a partir das minhas tarefas pendentes e das minhas preferências pessoais.

Projeto P0 do curso ("Primeiro fluxo com LLM"). A aplicação usa a API do **Google Gemini** para interpretar texto livre e gerar um plano do dia que concilia o que a pessoa *precisa* fazer com os hábitos de que ela *não abre mão*.

É também o primeiro módulo de um assistente pessoal maior (um "Jarvis"), que será evoluído nos próximos projetos.

## Por que um LLM?

As tarefas e preferências chegam em linguagem natural ("academia de manhã", "revisar o artigo até sexta", "ler antes de dormir"). Encaixar isso numa rotina exige interpretar texto ambíguo e equilibrar preferências subjetivas, algo que regras fixas fazem mal e um modelo de linguagem faz bem.

## Funcionalidades (nível básico)

Menu interativo no terminal com três seções:

| Seção | O que faz |
|---|---|
| **Perfil** | Mostra seus hábitos e preferências. Para criar ou editar, você descreve em texto livre e o LLM gera um resumo organizado. |
| **Tarefas** | Mostra suas tarefas pendentes. Para criar ou editar, você descreve em texto livre e o LLM organiza a lista. |
| **Plano do dia** | Gera uma rotina do dia combinando perfil + tarefas. Também permite pedir ajustes no plano. |

Os dados ficam em arquivos de texto locais na pasta `data/` (ignorada pelo Git, por conter informações pessoais).

## Requisitos

- Python **3.12+ ou superior** (o código usa `match/case`)
- Uma chave da API do Gemini (gratuita no [Google AI Studio](https://aistudio.google.com/))

## Instalação

```bash
git clone https://github.com/AndreyHenrique/TrendsIA-p0.git
cd TrendsIA-p0

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuração do acesso ao LLM

1. Gere uma chave em [Google AI Studio](https://aistudio.google.com/) → **Get API key**.
2. Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua-chave-aqui
GEMINI_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent
```

- `GEMINI_API_KEY`: sua chave (enviada no cabeçalho `X-goog-api-key`).
- `GEMINI_URL`: endpoint REST `generateContent` do modelo. Para usar outro modelo, troque o nome na URL (confira os disponíveis no AI Studio).

> ⚠️ O `.env` está no `.gitignore`. **Nunca** faça commit da sua chave.

**Provedor escolhido:** Google Gemini API (não o LLM institucional). Eventuais custos são de responsabilidade do usuário; a cota gratuita do modelo Flash é suficiente para o uso deste projeto.

## Execução

```bash
python main.py
```

Navegue com as setas e confirme com Enter. Ordem sugerida no primeiro uso: **Perfil → Criar**, **Tarefas → Criar**, **Plano do dia → Criar**.

## Exemplo de uso

**Perfil (entrada):**
```
Acordo às 6h, vou para a academia todo dia de manhã e gosto de ler antes de dormir.
```

**Tarefas (entrada):**
```
Revisar o artigo, estudar para a prova de banco de dados e fazer a lista de compras.
```

**Plano do dia (saída, resumida):**
```
Bom dia! Aqui está sua rotina de hoje:
06:00 – Acordar e café da manhã
06:30 – Academia
08:30 – Estudar para a prova de banco de dados (foco total pela manhã)
...
22:30 – Leitura antes de dormir
```

*(A saída real varia a cada execução, pois é gerada pelo modelo.)*

## Estrutura do projeto

```
TrendsIA-p0/
├── main.py           # menu e fluxo de cada seção
├── llm_client.py     # requisição HTTP à API do Gemini
├── dados.py          # leitura e gravação de perfil, tarefas e plano
├── requirements.txt
├── .gitignore
└── data/             # criada automaticamente (não versionada)
```

## Bibliotecas

| Biblioteca | Uso |
|---|---|
| `httpx` | requisições REST à API do Gemini |
| `python-dotenv` | carregar a chave e a URL do `.env` |
| `questionary` | menus e entradas interativas no terminal |

## Limitações conhecidas (a evoluir)

Esta é a versão **básica** (`p0-basico`). Ainda não há:

- tratamento amigável de erros (chave ausente/inválida, timeout, API indisponível);
- validação de entradas vazias;
- testes automatizados e configuração externa de parâmetros do modelo.

Esses pontos entram nas versões `p0-intermediario` e `p0-avancado`.

## Próximos passos (fora do escopo do P0)

- Integração com Notion e Google Calendar como fontes de tarefas;
- Execução agendada (plano enviado automaticamente toda noite);
- Planejamento semanal.

## Uso de IA no desenvolvimento

Ferramentas de IA (Claude) foram usadas para discutir o escopo do projeto, sugerir a estrutura de módulos e revisar o código. A implementação foi totalmente feita por mim.
