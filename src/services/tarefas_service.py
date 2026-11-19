import questionary
from src.repositories.arquivo_repository import carregar, salvar
from src.llm.llm_client import chamar_llm
from src.services.utils_service import sub_menu

def atualizar_tarefas(conteudo):
    salvar("tarefas", conteudo)
    questionary.print(
        text="Suas tarefas foram salvas com sucesso."
    )

def menu_tarefas():
    tarefas = carregar("tarefas")
    
    # Mostra um resumo do seu perfil
    questionary.print(
        text=tarefas if tarefas else "Você ainda não preencheu suas tarefas."
    )

    # Menu com:
    opcao = sub_menu("Tarefas", ["Editar" if tarefas else "Criar"])
    match opcao:
        # Opção 1: Pedir para editar ou criar   
        case "Editar":
            tarefas_input = questionary.text(
                message="Digite o que você gostaria de modificar:"
            ).ask()
 
            if not tarefas_input: return
    
            resposta = chamar_llm(
                message=tarefas_input,
                system_instructin=(
                    "Você é uma IA que analisa textos e retorna apenas um resumo sobre as tarefas do usuário "
                    "Você deve editar o seguinte texto para englobar as novas alterações do usuário. "
                    f"Resumo anterior: {tarefas}")
            )
            atualizar_tarefas(resposta)
            
        case "Criar":
            tarefas_input = questionary.text(
                message="Descreva suas tarefas pendentes:"
            ).ask()
            
            if not tarefas_input: return
 
            resposta = chamar_llm(
                message=tarefas_input,
                system_instructin=(
                    "Você é uma IA que analisa textos e retorna apenas um resumo sobre as tarefas do usuário")
            )
            
            atualizar_tarefas(resposta)
            
        # Opção 2: Voltar
        case _:
            pass 
