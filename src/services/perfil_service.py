from typing import override
from src.services.base_service import SecaoService        

class PerfilService(SecaoService):
    nome = "perfil"
    titulo = "Perfil"
    create_msg = "Descreva seus hábitos diários e preferências pessoais: "
    empty_msg = "Seu perfil ainda não foi criado. "
    
    @property
    @override
    def prompt_criar(self):
        return (
                "Você é uma IA que analisa textos e retorna apenas um resumo sobre os hábitos diários e "
                "de coisas que aquela pessoa não abre mão na rotina. "
            )
    
    @property
    @override
    def prompt_editar(self):
        return (
                "Você é uma IA que analisa textos e retorna apenas um resumo sobre os hábitos diários e "
                "de coisas que aquela pessoa não abre mão na rotina. "
                "Você deve editar o seguinte texto para englobar as novas alterações do usuário. "
                
                f"Resumo anterior: {self.obter()}"
            )