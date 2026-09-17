"""Moteur de recherche lexical TF-IDF word + char."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import Normalizer

from src.data import charger_fiches


@dataclass
class ResultatRecherche:
    fiche_id: int
    score: float
    titre: str
    url: str
    extrait: str


def construire_pipeline_tfidf() -> Pipeline:
    """Pipeline scikit-learn : FeatureUnion word + char, puis normalisation L2."""
    vectoriseur = FeatureUnion(
        [
            (
                "caracteristiques_mots",
                TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 2),
                    strip_accents="unicode",
                    lowercase=True,
                    max_df=0.95,
                ),
            ),
            (
                "caracteristiques_caracteres",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    strip_accents="unicode",
                    lowercase=True,
                    max_df=0.95,
                ),
            ),
        ]
    )
    return Pipeline(
        [
            ("caracteristiques", vectoriseur),
            ("normalisation", Normalizer(copy=False)),
        ]
    )


class MoteurRechercheFiches:
    """Index TF-IDF des fiches fiscales via FeatureUnion scikit-learn."""

    def __init__(self, fiches_df: pd.DataFrame | None = None):
        self.fiches_df = fiches_df if fiches_df is not None else charger_fiches()
        self.pipeline = construire_pipeline_tfidf()
        texts = self.fiches_df["search_text"].fillna("").astype(str)
        self.doc_matrix = self.pipeline.fit_transform(texts)

    def _vectoriser_question(self, question: str):
        return self.pipeline.transform([question])



    def rechercher(
        self, question: str, nombre_resultats: int = 5
    ) -> list[ResultatRecherche]:
        if not question or not question.strip():
            return []

        vecteur_question = self._vectoriser_question(question.strip())
        scores = cosine_similarity(vecteur_question, self.doc_matrix).flatten()
        nombre_resultats = min(nombre_resultats, len(scores))
        meilleurs_indices = np.argpartition(
            -scores, range(nombre_resultats)
        )[:nombre_resultats]
        meilleurs_indices = meilleurs_indices[np.argsort(-scores[meilleurs_indices])]

        resultats: list[ResultatRecherche] = []
        for idx in meilleurs_indices:
            fiche = self.fiches_df.iloc[int(idx)]
            extrait = fiche.Texte[:400] + ("…" if len(fiche.Texte) > 400 else "")
            resultats.append(
                ResultatRecherche(
                    fiche_id=int(fiche.fiche_id),
                    score=float(scores[idx]),
                    titre=fiche.Titre,
                    url=fiche.URL,
                    extrait=extrait,
                )
            )
        return resultats
