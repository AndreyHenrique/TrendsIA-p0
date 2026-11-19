import questionary 
from llm_client import chamar_llm
from dados import save_perfil, get_perfil, get_tarefas, save_tarefas, get_plano, save_plano

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

def atualizar_tarefas(conteudo):
    save_tarefas(conteudo)
    questionary.print(
        text="Suas tarefas foram salvas com sucesso."
    )

def menu_tarefas():
    tarefas = get_tarefas()
    
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

def atualizar_plano(conteudo):
    save_plano(conteudo)
    questionary.print(
        text="Seu plano foi salvo com sucesso"
    )

def menu_plano():
    plano = get_plano()
    perfil = get_perfil()
    tarefas = get_tarefas()
    
    # Mostra o plano, caso exista
    questionary.print(
        text=plano if plano else "Você ainda não possui um plano"
    )

    if not perfil or not tarefas:
        questionary.print(
            text="Por favor, preencha seu perfil e suas tarefas antes de tentar criar um plano."
        )
        return  

    # Menu com:
    opcao = sub_menu("Plano", ["Editar" if plano else "Criar"])
    match opcao:
        # Opção 1: Pedir para editar ou criar   
        
        case "Editar":
            plano_input = questionary.text(
                message="Digite o que você gostaria de modificar:"
            ).ask()
 
            if not plano_input: return
 
            resposta = chamar_llm(
                message= plano_input + (
                        f"Meu perfil e meus gostos: {perfil}. "
                        f"Atividades que eu preciso fazer: {tarefas}."
                    ),
                system_instructin=(
                    "Você é uma IA especialista em unir gostos pessoais do usuário com as atividades que ele tem para fazer. "
                    "Você vai atuar como o Jarvis do Homem de Ferro. "
                    "Você deve conciliar o perfil do usuário com o que ele precisa fazer."
                    "Você deve responder o usuário com toda a rotina dele durante o dia "
                    
                    "O usuário pediu que você modificasse o plano que você fez anteriormente"
                    
                    f"Plano anterior: {plano}. Justificativa do usuário: {plano_input}"
                    
                    f"Perfil e gostos do usuário: {perfil}. "
                    f"Atividades que o usuário precisa fazer: {tarefas}. "
                )
            )
            atualizar_plano(resposta)
            
        case "Criar":
            resposta = chamar_llm(
                message=(
                    f"Meu perfil e meus gostos: {perfil}. "
                    f"Atividades que eu preciso fazer: {tarefas}."
                ),
                system_instructin=(
                    "Você é uma IA especialista em unir gostos pessoais do usuário com as atividades que ele tem para fazer. "
                    "Você vai atuar como o Jarvis do Homem de Ferro. "
                    "Você deve conciliar o perfil do usuário com o que ele precisa fazer."
                    "Você deve responder o usuário com toda a rotina dele durante o dia "
                )
            )
            
            atualizar_plano(resposta)
            
        # Opção 2: Voltar
        case _:
            pass 

if __name__ == "__main__":
    main()