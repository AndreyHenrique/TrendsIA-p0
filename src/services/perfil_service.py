import questionary
from src.llm.llm_client import chamar_llm

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
 
            if not perfil_input: return
 
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
            
            if not perfil_input: return
 
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