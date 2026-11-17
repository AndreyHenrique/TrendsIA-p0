import questionary 

def main():
    
    while True:
        opcao = questionary.select(
            message="O que você quer fazer?",
            choices=["Perfil", "Tarefas", "Plano do dia"]
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

def menu_perfil():
    pass 

def menu_tarefas():
    pass 

def menu_plano():
    pass 

if __name__ == "__main__":
    main()