"""Tratamento centralizado de exceções de E/S, exibindo mensagens claras."""
import csv
import json


class BackupError(Exception):
    """Falha ao criar o backup; a escrita é cancelada para proteger os dados."""


def tratar_erro(erro, caminho=""):
    """Imprime uma mensagem clara de acordo com o tipo de erro."""
    if isinstance(erro, FileNotFoundError):
        msg = f"O arquivo '{caminho}' não foi encontrado. Verifique o caminho informado."
    elif isinstance(erro, PermissionError):
        msg = f"Sem permissão para acessar ou modificar '{caminho}'."
    elif isinstance(erro, IsADirectoryError):
        msg = f"'{caminho}' é uma pasta, não um arquivo."
    elif isinstance(erro, UnicodeError):
        msg = (f"Erro de codificação em '{caminho}'. O arquivo deve estar em UTF-8. "
               f"Detalhe: {erro}")
    elif isinstance(erro, json.JSONDecodeError):
        msg = (f"O arquivo '{caminho}' não é um JSON válido "
               f"(linha {erro.lineno}, coluna {erro.colno}): {erro.msg}")
    elif isinstance(erro, csv.Error):
        msg = f"O arquivo '{caminho}' não é um CSV válido: {erro}"
    elif isinstance(erro, BackupError):
        msg = f"Backup falhou, operação cancelada para proteger os dados: {erro}"
    elif isinstance(erro, ValueError):
        msg = f"Dados inválidos em '{caminho}': {erro}"
    elif isinstance(erro, OSError):
        msg = f"Erro de entrada/saída com '{caminho}': {erro}"
    else:
        msg = f"Erro inesperado: {erro}"
    print(f"[ERRO] {msg}")
    return msg


def executar_seguro(funcao, *args, caminho="", **kwargs):
    """Executa 'funcao' e trata exceções sem encerrar a aplicação.
    Retorna (True, resultado) em caso de sucesso e (False, None) em caso de erro."""
    try:
        return True, funcao(*args, **kwargs)
    except Exception as erro:  # a aplicação não deve encerrar inesperadamente
        tratar_erro(erro, caminho)
        return False, None
