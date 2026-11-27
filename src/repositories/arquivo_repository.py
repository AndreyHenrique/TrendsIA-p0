from pathlib import Path
from src.exceptions import RepositorioError

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
        
    try: 
        conteudo = caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise RepositorioError(
            f"Não foi possível ler os dados salvos ({caminho.name}). "
            "Verifique se o arquivo não está aberto em outro programa ou corrompido."
        ) from e
        
    return conteudo

def salvar(key: str, content: str) -> None:
    caminho = Path(DATA_DIR / ARQUIVOS[key])
    
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(content, encoding="utf-8")
    except (OSError) as e:
        raise RepositorioError(
            f"Não foi possível salvar os dados ({caminho.name}). "
            "Verifique as permissões da pasta data/ e o espaço em disco."
        ) from e