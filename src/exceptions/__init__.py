from src.exceptions.base import AppError
from src.exceptions.service_exceptions import DadosIncompletosError
from src.exceptions.repository_exceptions import RepositorioError
from src.exceptions.llm_client_exceptions import (
    LlmError,
    UrlAusenteError,
    UrlInvalidaError,
    CredencialAusenteError,
    CredencialInvalidaError,
    ServicoIndisponivelError,
    FalhaComunicacaoError,
    RespostaInesperadaError,
    TimeoutLlmError
)