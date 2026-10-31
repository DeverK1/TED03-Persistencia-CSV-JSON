"""Conversão entre CSV e JSON."""
from .escrita import escrever_csv, escrever_json
from .leitura import ler_csv, ler_json


def csv_para_json(caminho_csv, caminho_json):
    registros = ler_csv(caminho_csv)
    escrever_json(caminho_json, registros)
    return registros


def json_para_csv(caminho_json, caminho_csv):
    registros = ler_json(caminho_json)
    escrever_csv(caminho_csv, registros)
    return registros
