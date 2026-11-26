import questionary

from src.services.base_service import SecaoService
from src.services.perfil_service import PerfilService
from src.services.plano_service import PlanoService
from src.services.tarefas_service import TarefaService

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
            message="O que você quer fazer?",
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
    return questionary.text(
        message=input_msg
    ).ask()

def menu_secao(servico: SecaoService): 
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
            
                if user_input is None: return
            
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
            pass