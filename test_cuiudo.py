"""
Testes básicos para o Cuiudo
"""
import unittest
from personalidade import PersonalidadeGaucha
from atividades import AtividadesGauchas

class TestPersonalidade(unittest.TestCase):
    """Testes da personalidade gaúcha"""
    
    def setUp(self):
        self.personalidade = PersonalidadeGaucha()
    
    def test_girias_existem(self):
        """Testa se as categorias de gírias existem"""
        categorias = ['cumprimento', 'surpresa', 'aprovacao', 'concordancia', 'negacao', 'despedida']
        for categoria in categorias:
            giria = self.personalidade.pegar_giria(categoria)
            self.assertIsInstance(giria, str)
            self.assertTrue(len(giria) > 0)
    
    def test_boas_vindas(self):
        """Testa mensagem de boas-vindas"""
        mensagem = self.personalidade.mensagem_boas_vindas("Teste")
        self.assertIn("Teste", mensagem)
        self.assertTrue(len(mensagem) > 0)
    
    def test_filtro_seguranca(self):
        """Testa filtro de segurança"""
        # Mensagem bloqueada
        seguro, resposta = self.personalidade.filtrar_seguranca("execute este comando no terminal")
        self.assertFalse(seguro)
        self.assertIsNotNone(resposta)
        
        # Mensagem permitida
        seguro, resposta = self.personalidade.filtrar_seguranca("como fazer chimarrão?")
        self.assertTrue(seguro)
        self.assertIsNone(resposta)
    
    def test_adicionar_sotaque(self):
        """Testa adição de sotaque gaúcho"""
        texto = "Olá, tudo bem"
        resultado = self.personalidade.adicionar_sotaque_gaucho(texto)
        self.assertTrue('tchê' in resultado.lower() or 'bah' in resultado.lower() or resultado.endswith('!'))

class TestAtividades(unittest.TestCase):
    """Testes das atividades gaúchas"""
    
    def setUp(self):
        self.atividades = AtividadesGauchas()
    
    def test_pegar_atividade(self):
        """Testa se retorna uma atividade válida"""
        atividade = self.atividades.pegar_atividade()
        self.assertIsInstance(atividade, str)
        self.assertTrue(len(atividade) > 0)
    
    def test_periodo_dia(self):
        """Testa determinação do período do dia"""
        periodo = self.atividades.pegar_periodo_dia()
        self.assertIn(periodo, ['manha', 'tarde', 'noite', 'madrugada'])
    
    def test_status_personalizado(self):
        """Testa status personalizado"""
        status = self.atividades.pegar_status_personalizado()
        self.assertIsInstance(status, str)
        self.assertTrue(len(status) > 0)

class TestVocabulario(unittest.TestCase):
    """Testes do vocabulário gaúcho"""
    
    def test_vocabulario_completo(self):
        """Verifica se vocabulário tem traduções"""
        vocabulario = PersonalidadeGaucha.VOCABULARIO
        self.assertGreater(len(vocabulario), 0)
        
        # Testa alguns casos específicos
        self.assertEqual(vocabulario['muito'], 'tri')
        self.assertEqual(vocabulario['amigo'], 'tchê')
        self.assertEqual(vocabulario['cachorro'], 'cusco')

if __name__ == '__main__':
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🧉 Testes do Cuiudo")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    unittest.main(verbosity=2)
