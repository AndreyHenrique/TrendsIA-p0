import os
from dotenv import load_dotenv
from src.exceptions import UrlAusenteError, CredencialAusenteError

def carregar_config():
    load_dotenv()

    base_url = os.getenv("GEMINI_URL")
    if not base_url:
        raise UrlAusenteError("GEMINI_URL não definida. Configure-a no arquivo .env.")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: 
        raise CredencialAusenteError("GEMINI_API_KEY não definida. Configure-a no arquivo .env.")
    
    return base_url, api_key