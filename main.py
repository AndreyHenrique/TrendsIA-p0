import questionary 
from llm_client import chamar_llm
from dados import save_perfil, get_perfil

def main():
    
    while True:
        opcao = questionary.select(
            message="O que você quer fazer?",
            choices=["Perfil", "Tarefas", "Plano do dia", "Sair..."]
        ).ask()
        
        match opcao: 
            # Opção 1: Adiciona/Ver as peculiaridades do perfil 
            case "Perfil": 
                menu_perfil()
            # Opção 2: Adiciona/Ver lista de tarefas da pessoa
            case "Tarefas":
                menu_tarefas()
            # Opção 3: Adicionar/Ver plano semanal organizado 
            case "Plano do dia":
                menu_plano()
            case _:
                break

def sub_menu(mensagem, opcoes):
    return questionary.select(
        message=mensagem,
        choices=opcoes + ["Voltar"]
    ).ask()
    
def menu_perfil():
    perfil = get_perfil()
    
    # Mostra um resumo do seu perfil
    questionary.print(
        text=perfil if perfil else "Seu perfil ainda não foi criado."
    )

    # Menu com:
    opcao = sub_menu("Perfil", ["Editar" if perfil else "Criar"])
    match opcao:
        # Opção 1: Pedir para editar ou criar   
        case "Editar":
            perfil_input = questionary.text(
                message="Digite o que você gostaria de modificar:"
            ).ask()
 
            resposta = chamar_llm(
                message=perfil_input,
                system_instructin=(
                    "Você é uma IA que analisa textos e retorna apenas um resumo sobre os hábitos diários e"
                    "de coisas que aquela pessoa não abre mão na rotina."
                    "Você deve editar o seguinte texto para englobar as novas alterações do usuário."
                    f"Resumo anterior: {perfil}")
            )
            
            save_perfil(resposta)
            questionary.print(
                text="Seus hábitos/preferências foram salvos com sucesso."
            )
            
        case "Criar":
            perfil_input = questionary.text(
                message="Descreva seus hábitos diários e preferências pessoais:"
            ).ask()
 
            resposta = chamar_llm(
                message=perfil_input,
                system_instructin=(
                    "Você é uma IA que analisa textos e retorna apenas um resumo sobre os hábitos diários e"
                    "de coisas que aquela pessoa não abre mão na rotina.")
            )
            
            save_perfil(resposta)
            questionary.print(
                text="Seus hábitos/preferências foram salvos com sucesso."
            )
            
        # Opção 2: Voltar
        case _:
            pass 


def menu_tarefas():
    # Mostra um resumo das suas tarefas
    
    # Menu com: 
    # Opção 1: Pedir para editar
    # Opção 2: Voltar
    pass 

def menu_plano():
    # Mostra um resumo do plano atual
    
    # Menu com: 
    # Opção 1: Pedir para editar 
    # Opção 2: Voltar
    pass 

if __name__ == "__main__":
    main()