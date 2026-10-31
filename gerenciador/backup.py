"""Backup automático executado antes de qualquer alteração em arquivo persistido."""
import os
from datetime import datetime

from .erros import BackupError

PASTA_BACKUP = "backups"


def criar_backup(caminho, pasta_backup=None):
    """Copia o arquivo original para a pasta de backups com data/hora.
    Retorna o caminho do backup, ou None se o arquivo ainda não existe."""
    pasta_backup = pasta_backup or PASTA_BACKUP
    if not os.path.exists(caminho):
        print(f"[BACKUP] '{caminho}' ainda não existe; nenhum backup necessário.")
        return None
    try:
        os.makedirs(pasta_backup, exist_ok=True)
        nome, extensao = os.path.splitext(os.path.basename(caminho))
        carimbo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        destino = os.path.join(pasta_backup, f"{nome}_{carimbo}{extensao}")
        with open(caminho, "rb") as origem:
            conteudo = origem.read()
        with open(destino, "wb") as copia:
            copia.write(conteudo)
    except OSError as erro:
        raise BackupError(str(erro)) from erro
    print(f"[BACKUP] Backup criado com sucesso: {destino}")
    return destino
