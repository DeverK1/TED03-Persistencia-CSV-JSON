"""Gerenciador de Persistência de Dados em CSV e JSON - menu interativo."""
import os
from pprint import pprint

from gerenciador.conversao import csv_para_json, json_para_csv
from gerenciador.erros import executar_seguro
from gerenciador.escrita import escrever_csv, escrever_json
from gerenciador.leitura import ler_csv, ler_json

MENU = """
===== Gerenciador de Persistência CSV/JSON =====
1 - Converter CSV -> JSON
2 - Converter JSON -> CSV
3 - Visualizar arquivo (CSV ou JSON)
4 - Adicionar registro a um arquivo (com backup automático)
0 - Sair
"""


def _ler_por_extensao(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    if ext == ".csv":
        return ler_csv(caminho)
    if ext == ".json":
        return ler_json(caminho)
    raise ValueError("extensão não suportada (use .csv ou .json)")


def _escrever_por_extensao(caminho, registros):
    if caminho.lower().endswith(".csv"):
        escrever_csv(caminho, registros)
    else:
        escrever_json(caminho, registros)


def opcao_converter(origem_csv):
    entrada = input("Arquivo de entrada: ").strip()
    saida = input("Arquivo de saída: ").strip()
    funcao = csv_para_json if origem_csv else json_para_csv
    ok, registros = executar_seguro(funcao, entrada, saida, caminho=entrada)
    if ok:
        print(f"[OK] Conversão concluída: {len(registros)} registros convertidos.")


def opcao_visualizar():
    caminho = input("Arquivo: ").strip()
    ok, registros = executar_seguro(_ler_por_extensao, caminho, caminho=caminho)
    if ok:
        print(f"{len(registros)} registros em '{caminho}':")
        pprint(registros, sort_dicts=False)


def opcao_adicionar():
    caminho = input("Arquivo a atualizar: ").strip()
    ok, registros = executar_seguro(_ler_por_extensao, caminho, caminho=caminho)
    if not ok:
        return
    campos = list(registros[0].keys()) if registros else []
    if not campos:
        campos = [c.strip() for c in input("Campos (separados por vírgula): ").split(",") if c.strip()]
    novo = {campo: input(f"  {campo}: ").strip() for campo in campos}
    registros.append(novo)
    executar_seguro(_escrever_por_extensao, caminho, registros, caminho=caminho)


def main():
    while True:
        print(MENU)
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            opcao_converter(True)
        elif opcao == "2":
            opcao_converter(False)
        elif opcao == "3":
            opcao_visualizar()
        elif opcao == "4":
            opcao_adicionar()
        elif opcao == "0":
            print("Encerrando. Até logo!")
            break
        else:
            print("[ERRO] Opção inválida.")


if __name__ == "__main__":
    main()
