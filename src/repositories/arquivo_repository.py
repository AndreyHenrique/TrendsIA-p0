from pathlib import Path

# Sobe 2 níveis no repositório
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def get_perfil():
    return ler(DATA_DIR / "perfil.txt")

def get_tarefas():
    return ler(DATA_DIR / "tarefas.txt")

def get_plano():
    return ler(DATA_DIR / "data/plano.txt")

def save_perfil(perfil_text):
    escrever(file_name=DATA_DIR / "perfil.txt", content=perfil_text)
    
def save_tarefas(tarefas_text):
    escrever(file_name=DATA_DIR / "tarefas.txt", content=tarefas_text)
    
def save_plano(plano_text):
    escrever(file_name=DATA_DIR / "plano.txt", content=plano_text)

def ler(file_name: str):
    caminho = Path(file_name)
    if not caminho.exists():
        return None
        
    conteudo = caminho.read_text(encoding="utf-8")
    return conteudo
    
def escrever(file_name: str, content):
    
    caminho = Path(file_name)
    
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(content, encoding="utf-8")