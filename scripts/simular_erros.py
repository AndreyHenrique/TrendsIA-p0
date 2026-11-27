"""
    python -m scripts.simular_erros
"""
import os

import httpx

from src.exceptions import AppError
from src.llm import llm_client
import src.config as config

URL_FALSA = "https://exemplo.invalido/v1/models/modelo:generateContent"
_post_original = httpx.post


def _resposta(status: int, json=None, texto=None):
    """Cria uma função que imita httpx.post devolvendo a resposta indicada."""
    def post_falso(url, **kwargs):
        req = httpx.Request("POST", url)
        if json is not None:
            return httpx.Response(status, json=json, request=req)
        return httpx.Response(status, text=texto or "", request=req)
    return post_falso


def _erro(excecao: Exception):
    """Cria uma função que imita httpx.post lançando a exceção indicada."""
    def post_falso(url, **kwargs):
        raise excecao
    return post_falso


def _ambiente(url=URL_FALSA, chave="chave-de-teste"):
    os.environ.pop("GEMINI_URL", None)
    os.environ.pop("GEMINI_API_KEY", None)
    if url:
        os.environ["GEMINI_URL"] = url
    if chave:
        os.environ["GEMINI_API_KEY"] = chave


SUCESSO = {"candidates": [{"content": {"parts": [{"text": "06:00 Acordar..."}]}}]}

CENARIOS = [
    ("Sucesso", {}, _resposta(200, json=SUCESSO)),
    ("Configuração ausente (sem GEMINI_URL)", {"url": None}, None),
    ("Configuração inválida (URL sem protocolo)", {"url": "exemplo.invalido"}, None),
    ("Credencial ausente (sem GEMINI_API_KEY)", {"chave": None}, None),
    ("Credencial inválida (HTTP 400 'API key')", {},
     _resposta(400, json={"error": {"code": 400, "message": "API key not valid."}})),
    ("Limite de uso (HTTP 429)", {},
     _resposta(429, json={"error": {"code": 429, "message": "Quota exceeded"}})),
    ("Serviço indisponível (HTTP 503)", {},
     _resposta(503, json={"error": {"code": 503, "message": "Overloaded"}})),
    ("Serviço indisponível (HTTP 502 em HTML)", {}, _resposta(502, texto="<html>Bad Gateway</html>")),
    ("Falha de comunicação (sem internet)", {}, _erro(httpx.ConnectError("sem rede"))),
    ("Timeout", {}, _erro(httpx.ReadTimeout("demorou"))),
    ("Resposta vazia", {}, _resposta(200, json={"candidates": [{"content": {"parts": [{"text": "  "}]}}]})),
    ("Resposta em formato inesperado (sem candidates)", {},
     _resposta(200, json={"promptFeedback": {"blockReason": "SAFETY"}})),
    ("Resposta ilegível (200 sem JSON)", {}, _resposta(200, texto="isto não é JSON")),
]


def main():
    config.load_dotenv = lambda *a, **k: None  # ignora o .env real durante a simulação
    print("Demonstração SIMULADA — nenhuma chamada real ao Gemini é feita.\n")

    for nome, env, post_falso in CENARIOS:
        _ambiente(**env)
        llm_client.httpx.post = post_falso or _post_original
        try:
            resultado = llm_client.chamar_llm("teste")
            print(f"[OK]   {nome}\n       -> resposta: {resultado}\n")
        except AppError as e:
            print(f"[ERRO] {nome}\n       -> {type(e).__name__}: {e}\n")

    llm_client.httpx.post = _post_original


if __name__ == "__main__":
    main()
