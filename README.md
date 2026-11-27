# TrendsIA — Planejador de Rotina com LLM

> **Problema:** montar, pelo terminal, um plano de rotina para o dia a partir das minhas tarefas pendentes e das minhas preferências pessoais.

Projeto P0 do curso ("Primeiro fluxo com LLM"). A aplicação usa a API do **Google Gemini** para interpretar texto livre e gerar um plano do dia que concilia o que a pessoa *precisa* fazer com os hábitos de que ela *não abre mão*.

É também o primeiro módulo de um assistente pessoal maior (um "Jarvis"), que será evoluído nos próximos projetos.

## Por que um LLM?

As tarefas e preferências chegam em linguagem natural ("academia de manhã", "revisar o artigo até sexta", "ler antes de dormir"). Encaixar isso numa rotina exige interpretar texto ambíguo e equilibrar preferências subjetivas, algo que regras fixas fazem mal e um modelo de linguagem faz bem.

## Funcionalidades

Menu interativo no terminal com três seções:

| Seção | O que faz |
|---|---|
| **Perfil** | Mostra seus hábitos e preferências. Para criar ou editar, você descreve em texto livre e o LLM gera um resumo organizado. |
| **Tarefas** | Mostra suas tarefas pendentes. Para criar ou editar, você descreve em texto livre e o LLM organiza a lista. |
| **Plano do dia** | Gera uma rotina do dia combinando perfil + tarefas. Também permite pedir ajustes no plano. |

Os dados ficam em arquivos de texto locais na pasta `data/` (ignorada pelo Git, por conter informações pessoais).

## Requisitos

- Python **3.12+** (o código usa `typing.override`)
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

**Provedor escolhido:** Google Gemini API, acessada pela interface REST `generateContent` (não o LLM institucional). Eventuais custos são de responsabilidade do usuário; a cota gratuita do modelo Flash é suficiente para este projeto.

1. Gere uma chave em [Google AI Studio](https://aistudio.google.com/) → **Get API key**.
2. Copie o arquivo de exemplo e preencha a chave:

```bash
# Linux/macOS
cp .env.example .env
# Windows (PowerShell)
Copy-Item .env.example .env
```

```env
GEMINI_API_KEY=sua-chave-aqui
GEMINI_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent
```

| Variável | Para que serve |
|---|---|
| `GEMINI_API_KEY` | Sua chave. É enviada no cabeçalho `X-goog-api-key` e nunca aparece no código, nos logs ou nas mensagens de erro. |
| `GEMINI_URL` | Endpoint REST do modelo. Para usar outro modelo, troque o nome na URL (confira os disponíveis no AI Studio). |

> ⚠️ O `.env` está no `.gitignore`. **Nunca** faça commit da sua chave. O `.env.example` contém apenas a URL e a chave em branco.

## Execução

```bash
python main.py
```

Navegue com as setas e confirme com Enter. Ordem sugerida no primeiro uso: **Perfil → Criar**, **Tarefas → Criar**, **Plano do dia → Criar**. Para sair, escolha **Sair...** ou pressione Ctrl+C no menu principal.

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
06:00 – Acordar e café da manhã
06:30 – Academia
08:30 – Estudar para a prova de banco de dados (foco total pela manhã)
...
22:30 – Leitura antes de dormir
Salvo com sucesso.
```

*(A saída real varia a cada execução, pois é gerada pelo modelo.)*

**Entrada inválida:**
```
? Descreva suas tarefas pendentes:
A entrada não pode ser vazia.
```

## Arquitetura

O código segue uma arquitetura em camadas, para que cada responsabilidade fique em um lugar só:

```
TrendsIA-p0/
├── main.py                          # ponto de entrada
├── src/
│   ├── config.py                    # carregamento da configuração (.env)
│   ├── ui/menus.py                  # captura da entrada e apresentação do resultado
│   ├── services/                    # regras de negócio e preparação da solicitação (prompts)
│   │   ├── base_service.py
│   │   ├── perfil_service.py
│   │   ├── tarefas_service.py
│   │   └── plano_service.py         # exige perfil e tarefas antes de gerar o plano
│   ├── llm/llm_client.py            # chamada ao modelo e tratamento da resposta
│   ├── repositories/arquivo_repository.py   # leitura e gravação em data/
│   └── exceptions/                  # erros previstos, com mensagens para o usuário
├── scripts/simular_erros.py         # demonstração simulada dos erros
├── .env.example
├── requirements.txt
└── data/                            # criada automaticamente (não versionada)
```

| Responsabilidade | Onde fica |
|---|---|
| Captura da entrada | `src/ui/menus.py` (`pedir_texto`, `sub_menu`) |
| Carregamento da configuração | `src/config.py` |
| Preparação da solicitação | `src/services/*` (prompts de cada seção) |
| Chamada ao modelo | `src/llm/llm_client.py` (`_enviar`) |
| Tratamento da resposta | `src/llm/llm_client.py` (`_verificar_status`, `_prepara_resposta_usuario`) |
| Apresentação do resultado | `src/ui/menus.py` (`menu_secao`) |

Os erros previstos herdam de `AppError` e são capturados em um único ponto (`menu_secao`): a mensagem é exibida e o programa **volta ao menu** em vez de encerrar com um traceback.

## Tratamento de erros

| Situação | Exceção | Mensagem exibida |
|---|---|---|
| Entrada vazia | (validação na UI) | A entrada não pode ser vazia. |
| `GEMINI_URL` ausente | `UrlAusenteError` | GEMINI_URL não definida. Configure-a no arquivo .env. |
| `GEMINI_URL` inválida | `UrlInvalidaError` | GEMINI_URL inválida. Verifique-a no arquivo .env. |
| Modelo inexistente (HTTP 404) | `UrlInvalidaError` | Modelo não encontrado. Confira o nome do modelo na GEMINI_URL. |
| `GEMINI_API_KEY` ausente | `CredencialAusenteError` | GEMINI_API_KEY não definida. Configure-a no arquivo .env. |
| Chave inválida (HTTP 400/401/403) | `CredencialInvalidaError` | Chave de API inválida. Verifique a GEMINI_API_KEY no .env. |
| Limite de uso (HTTP 429) | `ServicoIndisponivelError` | Limite de uso da API atingido. Aguarde um pouco e tente novamente. |
| Serviço fora do ar (HTTP 5xx) | `ServicoIndisponivelError` | O serviço está indisponível no momento (503). Tente novamente. |
| Sem internet / DNS | `FalhaComunicacaoError` | Não foi possível conectar ao serviço. Verifique sua internet. |
| Timeout (60 s) | `TimeoutLlmError` | O modelo demorou demais para responder. Tente novamente. |
| Resposta vazia | `RespostaInesperadaError` | O modelo retornou uma resposta vazia. |
| Resposta fora do formato | `RespostaInesperadaError` | O modelo retornou uma resposta em formato inesperado. |
| Resposta que não é JSON | `RespostaInesperadaError` | O serviço retornou uma resposta ilegível. |
| Plano sem perfil/tarefas | `DadosIncompletosError` | Por favor, preencha seu perfil e suas tarefas antes de tentar criar um plano. |
| Erro ao ler/gravar `data/` | `RepositorioError` | Não foi possível ler/salvar os dados (...). |
| Ctrl+C durante uma operação | — | Operação cancelada. |

Nenhuma mensagem mostra a chave ou o corpo bruto da resposta da API.

## Testes realizados

### Testes reais (API do Gemini de verdade)

| Cenário | Como reproduzir | Resultado |
|---|---|---|
| Fluxo normal | `.env` correto → Perfil, Tarefas e Plano → Criar | Plano gerado e salvo |
| Credencial ausente | Deixe `GEMINI_API_KEY=` vazio no `.env` | `GEMINI_API_KEY não definida. Configure-a no arquivo .env.` |
| Credencial inválida | Use `GEMINI_API_KEY=chave-invalida-123` | `Chave de API inválida. Verifique a GEMINI_API_KEY no .env.` (a API respondeu HTTP 400 "API key not valid") |
| Configuração ausente | Renomeie o `.env` | `GEMINI_URL não definida. Configure-a no arquivo .env.` |
| Modelo inexistente | Troque o nome do modelo na `GEMINI_URL` por `modelo-que-nao-existe` | `Modelo não encontrado. Confira o nome do modelo na GEMINI_URL.` |
| Sem internet | Desconecte a rede e gere um plano | `Não foi possível conectar ao serviço. Verifique sua internet.` |
| Entrada vazia | Pressione Enter sem digitar nada | `A entrada não pode ser vazia.` (nenhuma chamada é feita) |

Em todos os casos o programa volta ao menu.

### Testes simulados (sem chamar a API)

Timeout, indisponibilidade (5xx) e respostas malformadas são difíceis de provocar de propósito. Por isso, `scripts/simular_erros.py` substitui a chamada HTTP por respostas falsas e mostra a mensagem que o usuário veria. Ele não usa sua chave nem acessa a internet.

```bash
python -m scripts.simular_erros
```

Saída:

```
[OK]   Sucesso
       -> resposta: 06:00 Acordar...
[ERRO] Configuração ausente (sem GEMINI_URL)
       -> UrlAusenteError: GEMINI_URL não definida. Configure-a no arquivo .env.
[ERRO] Configuração inválida (URL sem protocolo)
       -> UrlInvalidaError: GEMINI_URL inválida. Verifique-a no arquivo .env.
[ERRO] Credencial ausente (sem GEMINI_API_KEY)
       -> CredencialAusenteError: GEMINI_API_KEY não definida. Configure-a no arquivo .env.
[ERRO] Credencial inválida (HTTP 400 'API key')
       -> CredencialInvalidaError: Chave de API inválida. Verifique a GEMINI_API_KEY no .env.
[ERRO] Limite de uso (HTTP 429)
       -> ServicoIndisponivelError: Limite de uso da API atingido. Aguarde um pouco e tente novamente.
[ERRO] Serviço indisponível (HTTP 503)
       -> ServicoIndisponivelError: O serviço está indisponível no momento (503). Tente novamente.
[ERRO] Serviço indisponível (HTTP 502 em HTML)
       -> ServicoIndisponivelError: O serviço está indisponível no momento (502). Tente novamente.
[ERRO] Falha de comunicação (sem internet)
       -> FalhaComunicacaoError: Não foi possível conectar ao serviço. Verifique sua internet.
[ERRO] Timeout
       -> TimeoutLlmError: O modelo demorou demais para responder. Tente novamente.
[ERRO] Resposta vazia
       -> RespostaInesperadaError: O modelo retornou uma resposta vazia.
[ERRO] Resposta em formato inesperado (sem candidates)
       -> RespostaInesperadaError: O modelo retornou uma resposta em formato inesperado.
[ERRO] Resposta ilegível (200 sem JSON)
       -> RespostaInesperadaError: O serviço retornou uma resposta ilegível.
```

## Bibliotecas

| Biblioteca | Uso |
|---|---|
| `httpx` | requisições REST à API do Gemini |
| `python-dotenv` | carregar a chave e a URL do `.env` |
| `questionary` | menus e entradas interativas no terminal |

## Limitações conhecidas (a evoluir)

Versão **intermediária** (`p0-intermediario`). Ainda não há:

- testes automatizados com `pytest`;
- parâmetros do modelo (temperatura, limite de tokens, timeout) configuráveis fora do código;
- logs de execução;
- validação em ambiente limpo documentada.

Esses pontos entram na versão `p0-avancado`.

## Próximos passos (fora do escopo do P0)

- Integração com Notion e Google Calendar como fontes de tarefas;
- Execução agendada (plano enviado automaticamente toda noite);
- Planejamento semanal.

## Uso de IA no desenvolvimento

Usei o Claude para discutir o escopo, sugerir a arquitetura em camadas e revisar o código. Também com ele, escrevi o script de simulação de erros (`scripts/simular_erros.py`) e a documentação dos testes. A implementação da aplicação foi feita por mim.
