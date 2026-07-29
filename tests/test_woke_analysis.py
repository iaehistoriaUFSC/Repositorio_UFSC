import unittest
import socket

import numpy as np
from gensim.models import KeyedVectors

import woke_analysis as analysis
import woke_launcher as launcher


def keyed_vectors(*tokens: str) -> KeyedVectors:
    model = KeyedVectors(vector_size=3)
    vectors = np.arange(1, len(tokens) * 3 + 1, dtype=np.float32).reshape(-1, 3)
    model.add_vectors(list(tokens), vectors)
    return model


class WokeAnalysisTests(unittest.TestCase):
    def test_normalize_token_preserves_portuguese_diacritics(self):
        self.assertEqual(analysis.normalize_token("  História  "), "história")
        self.assertEqual(analysis.normalize_token("MEMÓRIA COLETIVA"), "memória_coletiva")

    def test_portuguese_and_spanish_tokens_remain_distinct(self):
        self.assertNotEqual(
            analysis.normalize_token("história"),
            analysis.normalize_token("historia"),
        )
        self.assertEqual(
            analysis.parse_tokens("história, historia"),
            ["história", "historia"],
        )

    def test_missing_tokens_reports_each_period(self):
        models = [
            ("WOKE_HST_2003_2010", keyed_vectors("história", "memória")),
            ("WOKE_HST_2011_2013", keyed_vectors("história")),
        ]

        self.assertEqual(
            analysis.missing_tokens_by_period(models, ["história", "memória"]),
            {"2011–2013": ["memória"]},
        )

    def test_require_tokens_has_readable_error(self):
        models = [("WOKE_HST_2003_2010", keyed_vectors("história"))]

        with self.assertRaisesRegex(ValueError, r"2003–2010: memória"):
            analysis.require_tokens(models, ["história", "memória"])

    def test_launcher_selects_an_available_local_port(self):
        port = launcher.available_port()
        self.assertIsInstance(port, int)
        self.assertGreater(port, 0)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.bind((launcher.HOST, port))


if __name__ == "__main__":
    unittest.main()
