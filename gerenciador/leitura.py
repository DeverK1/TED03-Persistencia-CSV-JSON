"""Rotinas de leitura de arquivos CSV e JSON."""
import csv
import json

ENCODING = "utf-8"


def ler_csv(caminho):
    """Lê um CSV e retorna uma lista de dicionários (um por linha)."""
    with open(caminho, "r", encoding=ENCODING, newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def ler_json(caminho):
    """Lê um JSON e retorna uma lista de registros (dicionários)."""
    with open(caminho, "r", encoding=ENCODING) as arquivo:
        dados = json.load(arquivo)
    if isinstance(dados, dict):
        dados = [dados]
    if not isinstance(dados, list) or not all(isinstance(r, dict) for r in dados):
        raise ValueError("o JSON deve conter uma lista de objetos (registros)")
    return dados
