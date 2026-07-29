"""Catálogo oficial dos pacotes WOKE publicados pelo projeto no Google Drive."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPackage:
    corpus: str
    mode: str
    rank: int
    file_id: str
    intervals: int
    known_download_bytes: int | None = None

    @property
    def key(self) -> str:
        return f"{self.corpus}|{self.mode}|{self.rank}"

    @property
    def label(self) -> str:
        return f"{self.display_corpus} — {self.mode} — Modelo {self.rank}"

    @property
    def display_corpus(self) -> str:
        names = {
            "UFSC 2003-2006": "UFSC — série completa 2003–2024",
            "HST-03-10": "História (HST) — série completa 2003–2024",
            "CFH-03-10": "CFH — série completa 2003–2024",
            "Saúde-Corpo-03-10": "Saúde e Corpo — série completa 2003–2024",
        }
        return names.get(self.corpus, self.corpus)

    @property
    def periods(self) -> tuple[str, ...]:
        if self.intervals == 10:
            ends = (2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024)
            if self.mode == "Temporal":
                return tuple(f"2003–{end}" for end in ends)
            starts = (2003, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023)
            return tuple(f"{start}–{end}" for start, end in zip(starts, ends))
        ends = (2010, 2013, 2016, 2019, 2024)
        if self.mode == "Temporal":
            return tuple(f"2003–{end}" for end in ends)
        starts = (2003, 2011, 2014, 2017, 2020)
        return tuple(f"{start}–{end}" for start, end in zip(starts, ends))

    @property
    def slug(self) -> str:
        corpus = self.corpus.lower().replace(" ", "-")
        mode = "inc" if self.mode == "Incremental" else "tmp"
        return f"{corpus}-{mode}-{self.rank}"


CATALOG = (
    ModelPackage("UFSC 2003-2006", "Incremental", 1, "1-p6Fik36eDbx1ezQs3dkrQop1_Hj-4qP", 10, 1_842_033_902),
    ModelPackage("UFSC 2003-2006", "Incremental", 2, "1wWkdQunoiOKl86UzIpdhpoFF4J9gbsxd", 10),
    ModelPackage("UFSC 2003-2006", "Incremental", 3, "1MOxnajuVYYRPOgK90bTX6ZwcKbe7f6gi", 10),
    ModelPackage("UFSC 2003-2006", "Incremental", 4, "1NBl-sCj5CQuG90zAGGYjcaJfRT8gJceq", 10),
    ModelPackage("UFSC 2003-2006", "Temporal", 1, "1domJgAtj-dNbIfUfi81Fimj8T9Zpc-RD", 10, 3_192_817_796),
    ModelPackage("UFSC 2003-2006", "Temporal", 2, "1xqGq9qUduFEkLn5lw_16Q4NpGcGdz22D", 10),
    ModelPackage("UFSC 2003-2006", "Temporal", 3, "1O-umkGjVr5Bh5y-llNviPec73ZOuNHJM", 10),
    ModelPackage("UFSC 2003-2006", "Temporal", 4, "1lQhwky-z3n2zcx6Neew8vvQXJ6ObM0Co", 10),
    ModelPackage("HST-03-10", "Incremental", 1, "1yRnVZJ-n6yl2gxSGGVpa5MmAj7SKMu_Q", 5, 25_791_889),
    ModelPackage("HST-03-10", "Incremental", 2, "1Q_JiD7vga-wziqQ4hIbqJeqUKB54h2aL", 5),
    ModelPackage("HST-03-10", "Incremental", 3, "1mNRbPDGUVEZRFRDxQhZYJyHWxYlYCEW2", 5),
    ModelPackage("HST-03-10", "Incremental", 4, "1nMoqj4o3caJBW76e6Ldh-IDjULsqvWrR", 5),
    ModelPackage("HST-03-10", "Temporal", 1, "1q3hKduwksarMpgPMp6KXzQ9R34Cc6-DU", 5, 37_049_113),
    ModelPackage("HST-03-10", "Temporal", 2, "1ZtzFwMFAfDw7sBkorU4LooxTS2GsHEkY", 5),
    ModelPackage("HST-03-10", "Temporal", 3, "1h9qQd4n3Ky9G-i_P6-CYNUWUTDFCX94Y", 5),
    ModelPackage("HST-03-10", "Temporal", 4, "1tRTMTF4INu3sD1mUoAOt7hHFvC869wlD", 5),
    ModelPackage("CFH-03-10", "Incremental", 1, "1E_Nif-V1msn_AocFPUC4HJGgwd0PUuI3", 5),
    ModelPackage("CFH-03-10", "Incremental", 2, "1RjXLPyq5jVnkQu33-CHa6qz3oTSA8-pu", 5),
    ModelPackage("CFH-03-10", "Incremental", 3, "1jCMGOK4tTHawZA6cWo0EJw1rsjWfy1mZ", 5),
    ModelPackage("CFH-03-10", "Temporal", 1, "10ndoZXudtCpgkc8-HKAF8O2xLNcIX09R", 5),
    ModelPackage("CFH-03-10", "Temporal", 2, "1ltkkII36Jwadgp2BR_cLyMXhqe7XLDGv", 5),
    ModelPackage("CFH-03-10", "Temporal", 3, "1jhLe-J01zPy5S8-hKx_oGyhoOrkQH6wz", 5),
    ModelPackage("Saúde-Corpo-03-10", "Incremental", 1, "1tEXGtfdABndYxbgXQ-x5wwZczTCfgpMx", 5),
    ModelPackage("Saúde-Corpo-03-10", "Incremental", 2, "1aopWw81GVsEUe6_jXTmxvpe83ZqYA1yq", 5),
    ModelPackage("Saúde-Corpo-03-10", "Incremental", 3, "1E1220ZYfc7MiVbmNUnE7U4hNDESUFgiP", 5),
    ModelPackage("Saúde-Corpo-03-10", "Temporal", 1, "12VY5FqkMrPkTxEfMjuLEPfRQ_PioTv-p", 5),
    ModelPackage("Saúde-Corpo-03-10", "Temporal", 2, "1ZjolluRy-nw33sYqzrPQrK2ZRCWE-op0", 5),
    ModelPackage("Saúde-Corpo-03-10", "Temporal", 3, "1GTXirosiGq7A0cYMXAZtU6u7pZD-JsAj", 5),
)

DEFAULT_KEYS = {
    "HST-03-10|Incremental|1",
    "HST-03-10|Temporal|1",
}


def package_by_key(key: str) -> ModelPackage:
    return next(package for package in CATALOG if package.key == key)
