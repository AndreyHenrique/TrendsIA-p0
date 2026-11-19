
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
