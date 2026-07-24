import unittest
from pathlib import Path

from src import motor
from src.app import Experiencia, StatusAmbiente, Visual
from src.modelos import ConjuntoGerado, Prompt, ResultadoPrompt


class TestUXCards(unittest.TestCase):
    def setUp(self):
        self.ui = Visual()
        self.experiencia = Experiencia(
            motor,
            StatusAmbiente(Path("."), "3", "Ollama local"),
            "ollama",
        )

    def test_status_normalizado(self):
        casos = {
            "pronto": "Pronto",
            "pronta": "Pronto",
            "concluido": "Pronto",
            "não concluída": "Erro",
            "erro": "Erro",
            "selecionado": "Selecionado",
        }

        for entrada, esperado in casos.items():
            with self.subTest(entrada=entrada):
                self.assertEqual(self.ui.status(entrada), esperado)

    def test_card_processo_mostra_resultado_antes_do_payload(self):
        html = self.ui.html_card_com_secoes(
            "Revisão Textual",
            {"Alternativa": 1, "Prompt": "P1", "Status": "Pronto"},
            [("Resultado", "Texto com ação")],
            [
                {"titulo": "System", "conteudo": "Sistema"},
                {"titulo": "Entrada", "conteudo": "Entrada"},
                {"titulo": "Payload LLM", "conteudo": {"saida": "ação"}},
            ],
        )

        self.assertLess(html.index("Resultado"), html.index("Payload LLM"))
        self.assertIn("ação", html)
        self.assertIn("<details class='pc-technical'>", html)
        abertura = html.split("<details class='pc-technical'", 1)[1].split(">", 1)[0]
        self.assertNotIn("open", abertura)

    def test_payload_llm_fica_no_final_dos_detalhes(self):
        html = self.ui.detalhes_tecnicos(
            [
                {"titulo": "Payload LLM", "conteudo": {"saida": "ok"}},
                {"titulo": "Entrada", "conteudo": "Entrada"},
                {"titulo": "System", "conteudo": "Sistema"},
            ]
        )

        self.assertLess(html.index("Entrada"), html.index("Payload LLM"))
        self.assertLess(html.index("System"), html.index("Payload LLM"))

    def test_rotulos_publicos_e_catalogos_usam_acentos(self):
        self.assertEqual(self.experiencia.rotulo_nome("cartao_ouro"), "Cartão Ouro")
        self.assertEqual(
            self.experiencia.rotulo_nome("familia_estabelecida"),
            "Família Estabelecida",
        )
        self.assertEqual(self.experiencia.rotulo_nome("Transformacao"), "Transformação")
        self.assertEqual(self.experiencia.rotulo_nome("AIDA"), "AIDA")
        self.assertEqual(
            self.experiencia.rotulo_etapa("revisor_textual"),
            "Revisão Textual",
        )

    def test_pipeline_tendencia_na_ordem_oficial(self):
        prompt = Prompt(
            grupo="3_tendencia_cognitiva",
            nome="p1",
            system="System",
            template="Template",
            origem="prompts/3_tendencia_cognitiva/p1.yaml",
        )
        conjunto = ConjuntoGerado(
            id="1",
            contexto={},
            tendencia="Afinidade",
            prompts={
                "tendencia_cognitiva": "3_tendencia_cognitiva/p1",
                "voz_bb": "4_voz_BB/p1",
                "tagline": "5_tagline/p1",
                "headline": "6_headline/p1",
                "cta": "7_cta/p1",
            },
            resultados=[
                ResultadoPrompt(
                    prompt=prompt,
                    system="System",
                    template_original="Template",
                    template_preenchido="Template preenchido",
                    entrada="Entrada",
                    opcao="Afinidade",
                    output="Texto",
                )
            ],
        )

        pipeline = self.experiencia.pipeline_conjunto(conjunto)
        esperado = [
            "Tendência P1",
            "Voz BB P1",
            "Tagline P1",
            "Headline P1",
            "CTA P1",
        ]

        posicoes = [pipeline.index(item) for item in esperado]
        self.assertEqual(posicoes, sorted(posicoes))


if __name__ == "__main__":
    unittest.main()
