from pathlib import Path

def get_perfil():
    return ler("data/perfil.txt")

def ler(file_name: str):
    caminho = Path(file_name)
    if not caminho.exists():
        return None
        
    conteudo = caminho.read_text(encoding="utf-8")
    return conteudo

def save_perfil(perfil_text):
    escrever(file_name="data/perfil.txt", content=perfil_text)
    
def escrever(file_name: str, content):
    
    caminho = Path(file_name)
    
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(content, encoding="utf-8")