import questionary
from src.llm.llm_client import chamar_llm

def sub_menu(mensagem, opcoes):
    return questionary.select(
        message=mensagem,
        choices=opcoes + ["Voltar"]
    ).ask()