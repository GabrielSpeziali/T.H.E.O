import unittest
from comandos import executar_comando

class TestComandosFixos(unittest.TestCase):
    def setUp(self):
        self.respostas = []

    def mock_falar(self, texto):
        self.respostas.append(texto)

    def mock_ouvir(self):
        return "não"  # simula o usuário dizendo "não" quando o comando não for reconhecido

    def test_comando_nome(self):
        executar_comando("seu nome", self.mock_falar, self.mock_ouvir)
        self.assertIn("Theo", " ".join(self.respostas))

    def test_comando_data(self):
        executar_comando("qual é a data de hoje", self.mock_falar, self.mock_ouvir)
        self.assertTrue(any("hoje é" in r.lower() for r in self.respostas))

    def test_comando_desconhecido(self):
        executar_comando("comando inventado", self.mock_falar, self.mock_ouvir)
        self.assertTrue(any("deseja me ensinar" in r.lower() for r in self.respostas))

if __name__ == '__main__':
    unittest.main()
