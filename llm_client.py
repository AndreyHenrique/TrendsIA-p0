import os
import httpx 
from dotenv import load_dotenv

def chamar_llm(message: str):
    
    load_dotenv()
    base_url = os.getenv("GEMINI_URL")
    api_key = os.getenv("GEMINI_API_KEY")
    
    resultado = httpx.post(
        base_url,
        headers={
            'X-goog-api-key' : api_key
        },
        json={
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
    
    return resultado.json()["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    print(chamar_llm("2+2"))