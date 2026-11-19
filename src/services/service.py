import questionary
from src.llm.llm_client import chamar_llm
from src.repositories.arquivo_repository import save_perfil, get_perfil, get_tarefas, save_tarefas, get_plano, save_plano

def sub_menu(mensagem, opcoes):
    return questionary.select(
        message=mensagem,
        choices=opcoes + ["Voltar"]
    ).ask()
    