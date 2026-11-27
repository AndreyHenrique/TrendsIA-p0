from src.exceptions.base import AppError

class LlmError(AppError):
    pass 


class UrlAusenteError(LlmError):
    pass 

class UrlInvalidaError(LlmError):
    pass 

class CredencialAusenteError(LlmError):
    pass

class CredencialInvalidaError(LlmError):
    pass 

class ServicoIndisponivelError(LlmError):
    pass 

class FalhaComunicacaoError(LlmError):
    pass

class TimeoutLlmError(LlmError):
    pass

class RespostaInesperadaError(LlmError):
    pass 