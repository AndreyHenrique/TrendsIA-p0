import os
import httpx 
from dotenv import load_dotenv

from src.exceptions import (
    UrlAusenteError, UrlInvalidaError, CredencialAusenteError, CredencialInvalidaError,
    ServicoIndisponivelError, FalhaComunicacaoError, RespostaInesperadaError
    )

def _carregar_config():
    load_dotenv()

    base_url = os.getenv("GEMINI_URL")
    if not base_url:
        raise UrlAusenteError("GEMINI_URL não definida. Configure-a no arquivo .env.")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: 
        raise CredencialAusenteError("GEMINI_API_KEY não definida. Configure-a no arquivo .env.")
    
    return base_url, api_key

def _enviar(base_url, api_key, message, system_instruction):
    try:
        resultado = httpx.post(
            base_url,
            headers={
                'X-goog-api-key' : api_key
            },
            json={
                "system_instruction" : {"parts": [{"text": system_instruction}]},
                "contents" : [
                    {
                        "parts" : [
                            {
                                "text" : message
                            }
                        ]
                    }
                ]
            },
            timeout=60
        )
    except (httpx.UnsupportedProtocol, httpx.InvalidURL) as e:
        raise UrlInvalidaError("GEMINI_URL inválida. Verifique-a no arquivo .env.") from e
    except httpx.TimeoutException as e: 
        raise FalhaComunicacaoError("O modelo demorou demais para responder. Tente novamente.") from e
    except httpx.RequestError as e:
        raise FalhaComunicacaoError("Não foi possível conectar ao serviço. Verifique sua internet.") from e
    
    return resultado

def _verificar_status(resp: httpx.Response) -> None:
    status = resp.status_code
    if resp.is_success: return 
    
    try:
        mensagem_error = resp.json().get("error", {}).get("message", "")
    except ValueError:
        mensagem_error =  "" 
    
    if status in (401, 403) or (status == 400 and "API key" in mensagem_error):
        raise CredencialInvalidaError("Chave de API inválida. Verifique a GEMINI_API_KEY no .env.")
    if status == 404:
        raise UrlInvalidaError("Modelo não encontrado. Confira o nome do modelo na GEMINI_URL.")
    if status == 429:
        raise ServicoIndisponivelError("Limite de uso da API atingido. Aguarde um pouco e tente novamente.")
    if status >= 500:
        raise ServicoIndisponivelError(f"O serviço está indisponível no momento ({status}). Tente novamente.")

    raise RespostaInesperadaError(f"O serviço recusou a requisição ({status}).")

def _prepara_resposta_usuario(resp: httpx.Response):
    
    # Valida json da respsota 
    try:
        dados = resp.json()
    except ValueError as e:
        raise RespostaInesperadaError("O serviço retornou uma resposta ilegível.") from e  
    
    # Válida formato da resposta
    try:
        candidato = dados["candidates"][0]
        resposta = "".join(
            p["text"] for p in candidato["content"]["parts"]
        )
    except (KeyError, IndexError, TypeError) as e:
        raise RespostaInesperadaError("O modelo retornou uma resposta em formato inesperado.") from e

    if not resposta.strip():
        raise RespostaInesperadaError("O modelo retornou uma resposta vazia.") 

    return resposta

def chamar_llm(message: str, system_instruction: str = ""):
    
    url, chave = _carregar_config()
    
    resp = _enviar(url, chave, message, system_instruction)  
        
    _verificar_status(resp=resp)
    
    return _prepara_resposta_usuario(resp)
            

if __name__ == "__main__":
    print(chamar_llm("2+2"))