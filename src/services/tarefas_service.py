from typing import override
from src.services.base_service import SecaoService

class TarefaService(SecaoService):
    nome = "tarefa"
    titulo = "Tarefa"
    create_msg = "Descreva suas tarefas pendentes: "
    empty_msg = "Você ainda não preencheu suas tarefas. "
    
    @property
    @override
    def prompt_criar(self):
        return ("Você é uma IA que analisa textos e retorna apenas um resumo sobre as tarefas do usuário")
    
    @property
    @override
    def prompt_editar(self):
        return (
                "Você é uma IA que analisa textos e retorna apenas um resumo sobre as tarefas do usuário "
                "Você deve editar o seguinte texto para englobar as novas alterações do usuário. "
                f"Resumo anterior: {self.obter()}"
            )