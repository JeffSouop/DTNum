from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_CSV = DATA_DIR / "info_particulier_impot.csv"
QUESTIONS_CSV = DATA_DIR / "questions_fiches_fip.csv"


class Fiche(NamedTuple):
    fiche_id: int
    titre: str
    url: str
    texte: str
    niveau_0: str
    niveau_1: str


def _nettoyer_texte(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\s+", " ", text.strip())
    return text


def charger_fiches(chemin_csv: Path | None = None) -> pd.DataFrame:
    """Charge les fiches pratiques et normalise les colonnes."""
    chemin = chemin_csv or DOCS_CSV
    df = pd.read_csv(chemin, encoding="utf-8")
    colonne_id = df.columns[0]
    df = df.rename(columns={colonne_id: "fiche_id"})
    df["fiche_id"] = df["fiche_id"].astype(int)
    df["Titre"] = df["Titre"].map(_nettoyer_texte)
    df["Texte"] = df["Texte"].map(_nettoyer_texte)
    df["URL"] = df["URL"].fillna("").astype(str)
    df["niveau_0"] = df["niveau_0"].fillna("").astype(str)
    df["niveau_1"] = df["niveau_1"].fillna("").astype(str)
    df["search_text"] = (df["Titre"] + ". " + df["Texte"]).map(_nettoyer_texte)
    return df


def charger_questions(chemin_csv: Path | None = None) -> pd.DataFrame:
    """Charge les questions d'évaluation avec la fiche attendue."""
    chemin = chemin_csv or QUESTIONS_CSV
    df = pd.read_csv(chemin, encoding="utf-8")
    colonne_index = df.columns[0]
    df = df.rename(columns={colonne_index: "question_id"})
    df["question"] = df["question"].map(_nettoyer_texte)
    df["num_texte"] = df["num_texte"].astype(int)
    return df


def convertir_fiches_en_objets(df: pd.DataFrame) -> list[Fiche]:
    return [
        Fiche(
            fiche_id=int(row.fiche_id),
            titre=row.Titre,
            url=row.URL,
            texte=row.Texte,
            niveau_0=row.niveau_0,
            niveau_1=row.niveau_1,
        )
        for row in df.itertuples(index=False)
    ]
