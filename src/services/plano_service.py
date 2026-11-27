from typing import override

from src.services.base_service import SecaoService
from src.services.perfil_service import PerfilService
from src.services.tarefas_service import TarefaService
from src.exceptions import DadosIncompletosError

class PlanoService(SecaoService):
    nome = "plano"
    titulo = "Plano"
    empty_msg = "Você ainda não possui um plano"
    use_create_msg = False
    
    def __init__(self, perfil: PerfilService, tarefa: TarefaService):
        self.perfil = perfil
        self.tarefa = tarefa
    
    @property
    def get_pedido_padrao(self):
        perfil = self.perfil.obter()
        tarefas = self.tarefa.obter()
        
        if not perfil or not tarefas:
            raise DadosIncompletosError("Por favor, preencha seu perfil e suas tarefas antes de tentar criar um plano.")
        
        pedido: str = (
                f"Perfil e gostos do usuário: {perfil}. "
                f"Atividades que o usuário precisa fazer: {tarefas}." 
            )
        return pedido
    
    @override
    def criar(self, entrada: str = "") -> str:
        return super().criar(self.get_pedido_padrao)
    
    @property
    @override
    def prompt_criar(self):
        return (
                "Você é uma IA especialista em unir gostos pessoais do usuário com as atividades que ele tem para fazer. "
                "Não adicione saudações, apenas retorne o resumo do plano para o usuário. "
                "Você deve conciliar o perfil do usuário com o que ele precisa fazer. "
                "Você deve responder o usuário com toda a rotina dele durante o dia "
            )
        
    @override
    def editar(self, pedido):
        pedido = (
                "O usuário pediu que você modificasse o plano que você fez anteriormente. "
                f"{self.get_pedido_padrao}"
                f"Plano anterior: {self.obter()}. Justificativa do usuário: {pedido}"
                )
        
        return super().editar(pedido)
    
    @property
    @override
    def prompt_editar(self):
        return (
                "Você é uma IA especialista em unir gostos pessoais do usuário com as atividades que ele tem para fazer. "
                "Não adicione saudações, apenas retorne o resumo do plano para o usuário. "
                "Você deve conciliar o perfil do usuário com o que ele precisa fazer. "
                "Você deve responder o usuário com toda a rotina dele durante o dia "
            )