import questionary

from src.services.base_service import SecaoService
from src.services.perfil_service import PerfilService
from src.services.plano_service import PlanoService
from src.services.tarefas_service import TarefaService
from src.exceptions import AppError

perfil = PerfilService()
tarefas = TarefaService()

SECOES = {
    "Perfil" : perfil,
    "Tarefas" : tarefas,
    "Plano do dia" : PlanoService(perfil=perfil, tarefa=tarefas)
}

def menu():
    while True:
        opcao = questionary.select(
            message="O que você quer ver?",
            choices=[*SECOES, "Sair..."]
        ).ask()
        
        if opcao is None or opcao == "Sair...": break 
        
        servico = SECOES[opcao]
        menu_secao(servico)

def sub_menu(mensagem, opcoes):
    return questionary.select(
        message=mensagem,
        choices=opcoes + ["Voltar"]
    ).ask()

def pedir_texto(input_msg):
    resposta = questionary.text(
        message=input_msg
    ).ask()
    
    if resposta is None: return
    
    if not resposta.strip(): 
        questionary.print("A entrada não pode ser vazia.", style="fg:yellow")
        return None
    
    return resposta

def menu_secao(servico: SecaoService): 
    
    try:
        data = servico.obter()

        # Mostra um resumo das informações já preenchidas, caso haja
        questionary.print(
            text=data if data else servico.empty_msg
        )

        # Carrega opções do serviço
        opcao = sub_menu(servico.titulo, servico.get_opcoes())


        match opcao:
            
            case "Criar":
                user_input = ""
                # Cria as informações da seção
                if servico.use_create_msg:
                    user_input = pedir_texto(servico.get_create_msg())
                    if not user_input: return
                
                servico.criar(user_input)
                
                questionary.print(
                    text="Salvo com sucesso.", style="fg:green"
                )
            case "Editar":
                user_input = pedir_texto(servico.get_update_msg())
                if not user_input: return
                
                # Edita as informações da seção
                servico.editar(user_input)
                
                questionary.print(
                    text="Atualizado com sucesso.", style="fg:green"
                )
                
            # Voltar
            case _:
                return 
            
    except AppError as e:
        questionary.print(str(e), style="fg:red")
    except KeyboardInterrupt:
        questionary.print("Operação cancelada", style="fg-yellow")