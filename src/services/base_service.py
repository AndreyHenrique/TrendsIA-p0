# src/services/base_service.py
from abc import ABC, abstractmethod
from src.llm.llm_client import chamar_llm
from src.repositories.arquivo_repository import carregar, salvar

class SecaoService(ABC):
    nome: str  # nome do arquivo no repositório: "perfil", "tarefas", "plano"
    titulo: str
    empty_msg: str
    create_msg: str
    use_create_msg: bool = True
    update_msg: str = "Digite o que você gostaria de modificar:"
    data: str = None
    
    @property
    @abstractmethod
    def prompt_criar(self) -> str: ...

    @property
    @abstractmethod
    def prompt_editar(self) -> str: ...

    # Obtém o conteúdo do serviço 
    def obter(self) -> str | None:
        if self.data is None:
            self.data = carregar(self.nome)
            
        return self.data

    # Cria conteúdo para o serviço
    def criar(self, entrada: str = "") -> str:
        return self._gerar(entrada, self.prompt_criar)

    # Edita o conteúdo para o serviço
    def editar(self, pedido: str) -> str:
        return self._gerar(pedido, self.prompt_editar)
    
    # Gera o conteúdo com a IA
    def _gerar(self, mensagem: str, prompt: str) -> str:
        resposta = chamar_llm(message=mensagem, system_instruction=prompt)
        salvar(self.nome, resposta)
        self.data = resposta
        return resposta
    
    # getters
    def get_opcoes(self) -> list:
        return ["Editar" if self.data else "Criar"]
    
    def get_create_msg(self) -> str:
        return self.create_msg

    def get_update_msg(self) -> str:
        return self.update_msg
    