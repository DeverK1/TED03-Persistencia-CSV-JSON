# TED 03 – Gerenciador de Persistência de Dados em Arquivos Estruturados (CSV e JSON)

**Instituição:** UniBalsas – Centro Universitário  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Disciplina:** Algoritmos e Programação Avançada  

**Integrantes (trio, com ciência do professor):**
- Kawê Victor Lima de Oliveira – MA 26.1.16277
- Luiz Fernando Carvalho da Costa – MA 26.1.13589
- Joacy Arruda de Assis Junior – MA 25.1.08341

## Descrição
Módulo em Python que lê, escreve, converte (CSV ⇄ JSON) e atualiza dados persistidos em arquivos, com
gerenciamento seguro de recursos (`with open(...)`, UTF-8), tratamento de exceções de E/S e **backup automático**
antes de qualquer alteração de arquivo.

## Funcionalidades
- Leitura de CSV e JSON (`gerenciador/leitura.py`)
- Escrita de CSV e JSON (`gerenciador/escrita.py`)
- Conversão CSV → JSON e JSON → CSV sem perda de registros/valores (`gerenciador/conversao.py`)
- Backup automático com data/hora em `backups/` antes de sobrescrever (`gerenciador/backup.py`); se o backup falhar, a escrita é cancelada
- Tratamento de `FileNotFoundError`, `PermissionError`, `UnicodeDecodeError`, JSON/CSV inválidos e outros `OSError`, com mensagens claras (`gerenciador/erros.py`)
- Menu interativo (`main.py`): converter, visualizar e adicionar registro

## Estrutura
```
main.py                  # menu interativo
gerenciador/             # módulos (leitura, escrita, conversao, backup, erros)
dados/                   # arquivos de teste (válidos e inválidos)
testes/test_gerenciador.py  # testes automatizados
backups/  saidas/        # gerados em execução
prints/                  # capturas de tela usadas no relatório
TED03_Relatorio_Kawe_Luiz_Joacy.pdf  # relatório técnico
```

## Como executar
Requer Python 3.8+ (somente biblioteca padrão).
```
python main.py
```
Exemplos de uso no menu:
- Opção 1: entrada `dados/alunos.csv`, saída `saidas/alunos.json`
- Opção 2: entrada `dados/produtos.json`, saída `saidas/produtos.csv`
- Opção 4: arquivo `saidas/alunos.json` (gera backup em `backups/` antes de gravar)
- Teste de erros: informe `nao_existe.csv` (opção 1), ou visualize (opção 3) `dados/invalido_latin1.csv` (erro de codificação) ou `dados/invalido.json`

## Como testar
```
python -m unittest discover -s testes -v
```

## Observações de projeto
- Valores do CSV são mantidos como texto na conversão, o que garante ida e volta sem perda (ex.: `007`, `10`, `9.0`).
- No JSON → CSV, campos aninhados são gravados como texto JSON e campos ausentes ficam vazios.
