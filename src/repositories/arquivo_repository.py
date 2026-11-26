from pathlib import Path

# Sobe 2 níveis no repositório
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

ARQUIVOS ={
    "perfil" : "perfil.txt",
    "tarefa" : "tarefas.txt",
    "plano" : "plano.txt"
}

def carregar(key: str) -> str:
    caminho = Path(DATA_DIR / ARQUIVOS[key])
    if not caminho.exists():
        return None
        
    conteudo = caminho.read_text(encoding="utf-8")
    return conteudo

def salvar(key: str, content: str) -> None:
    caminho = Path(DATA_DIR / ARQUIVOS[key])
    
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(content, encoding="utf-8")
