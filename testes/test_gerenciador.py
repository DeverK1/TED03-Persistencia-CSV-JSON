import json, os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gerenciador import backup
from gerenciador.conversao import csv_para_json, json_para_csv
from gerenciador.erros import executar_seguro
from gerenciador.escrita import escrever_json
from gerenciador.leitura import ler_csv, ler_json

DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")


class TestGerenciador(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        backup.PASTA_BACKUP = os.path.join(self.tmp, "bk")

    def p(self, nome):
        return os.path.join(self.tmp, nome)

    def test_csv_para_json_preserva_dados(self):
        saida = self.p("a.json")
        csv_para_json(os.path.join(DADOS, "alunos.csv"), saida)
        self.assertEqual(ler_json(saida), ler_csv(os.path.join(DADOS, "alunos.csv")))
        self.assertEqual(ler_json(saida)[0]["nome"], "João Antônio")

    def test_json_para_csv_preserva_registros(self):
        original = ler_json(os.path.join(DADOS, "produtos.json"))
        csv_path = self.p("p.csv")
        json_para_csv(os.path.join(DADOS, "produtos.json"), csv_path)
        linhas = ler_csv(csv_path)
        self.assertEqual(len(linhas), len(original))
        self.assertEqual(linhas[1]["descricao"], "Pão de Queijo Congelado")

    def test_backup_criado_antes_de_sobrescrever(self):
        alvo = self.p("x.json")
        escrever_json(alvo, [{"v": 1}])
        escrever_json(alvo, [{"v": 2}])
        copias = os.listdir(backup.PASTA_BACKUP)
        self.assertEqual(len(copias), 1)
        with open(os.path.join(backup.PASTA_BACKUP, copias[0]), encoding="utf-8") as f:
            self.assertEqual(json.load(f), [{"v": 1}])

    def test_arquivo_inexistente(self):
        ok, _ = executar_seguro(ler_csv, self.p("nao_existe.csv"), caminho="nao_existe.csv")
        self.assertFalse(ok)

    def test_erro_de_codificacao(self):
        ok, _ = executar_seguro(ler_csv, os.path.join(DADOS, "invalido_latin1.csv"))
        self.assertFalse(ok)

    def test_json_invalido(self):
        ok, _ = executar_seguro(ler_json, os.path.join(DADOS, "invalido.json"))
        self.assertFalse(ok)

    def test_pasta_no_lugar_de_arquivo(self):
        ok, _ = executar_seguro(ler_csv, self.tmp)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)
