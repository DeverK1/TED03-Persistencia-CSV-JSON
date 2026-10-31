"""Rotinas de escrita em CSV e JSON, sempre precedidas de backup."""
import csv
import json

from .backup import criar_backup
from .leitura import ENCODING


def _campos(registros):
    """União ordenada de todos os campos presentes nos registros."""
    campos = []
    for registro in registros:
        for chave in registro:
            if chave not in campos:
                campos.append(chave)
    return campos


def escrever_json(caminho, registros):
    criar_backup(caminho)  # backup ANTES de alterar
    with open(caminho, "w", encoding=ENCODING) as arquivo:
        json.dump(registros, arquivo, ensure_ascii=False, indent=4)
    print(f"[OK] JSON gravado em '{caminho}' ({len(registros)} registros).")


def escrever_csv(caminho, registros):
    criar_backup(caminho)  # backup ANTES de alterar
    campos = _campos(registros)
    with open(caminho, "w", encoding=ENCODING, newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos, restval="")
        escritor.writeheader()
        for registro in registros:
            linha = {}
            for chave, valor in registro.items():
                if valor is None:
                    linha[chave] = ""
                elif isinstance(valor, (dict, list)):
                    linha[chave] = json.dumps(valor, ensure_ascii=False)
                else:
                    linha[chave] = valor
            escritor.writerow(linha)
    print(f"[OK] CSV gravado em '{caminho}' ({len(registros)} registros).")
