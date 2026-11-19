from pathlib import Path

def get_perfil():
    return ler("data/perfil.txt")

def get_tarefas():
    return ler("data/tarefas.txt")

def get_plano():
    return ler("data/plano.txt")


def ler(file_name: str):
    caminho = Path(file_name)
    if not caminho.exists():
        return None
        
    conteudo = caminho.read_text(encoding="utf-8")
    return conteudo

def save_perfil(perfil_text):
    escrever(file_name="data/perfil.txt", content=perfil_text)
    
def save_tarefas(tarefas_text):
    escrever(file_name="data/tarefas.txt", content=tarefas_text)
    
def save_plano(plano_text):
    escrever(file_name="data/plano.txt", content=plano_text)
    
def escrever(file_name: str, content):
    
    caminho = Path(file_name)
    
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(content, encoding="utf-8")