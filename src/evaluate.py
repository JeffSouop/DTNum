"""Évaluation du moteur de recherche sur le jeu de questions annotées."""

from __future__ import annotations

from dataclasses import dataclass

from src.data import charger_questions
from src.retrieval import MoteurRechercheFiches


@dataclass
class MetriquesEvaluation:
    n_questions: int
    top1: float
    top3: float
    top5: float

    def en_dictionnaire(self) -> dict[str, float | int]:
        return {
            "n_questions": self.n_questions,
            "top1": self.top1,
            "top3": self.top3,
            "top5": self.top5,
        }


def evaluer_moteur(moteur: MoteurRechercheFiches) -> MetriquesEvaluation:
    """Calcule la précision top-1, top-3 et top-5 sur tout le jeu annoté."""
    questions = charger_questions()
    nombre_resultats_max = 5
    hits = {1: 0, 3: 0, 5: 0}
    n = len(questions)

    for question in questions.itertuples(index=False):
        fiche_attendue = int(question.num_texte)
        resultats = moteur.rechercher(
            question.question, nombre_resultats=nombre_resultats_max
        )
        ids_classes = [r.fiche_id for r in resultats]

        for k in (1, 3, 5):
            if fiche_attendue in ids_classes[:k]:
                hits[k] += 1

    return MetriquesEvaluation(
        n_questions=n,
        top1=hits[1] / n if n else 0.0,
        top3=hits[3] / n if n else 0.0,
        top5=hits[5] / n if n else 0.0,
    )


def lancer_evaluation_cli() -> None:
    moteur = MoteurRechercheFiches()
    metriques = evaluer_moteur(moteur)
    print(f"Questions évaluées : {metriques.n_questions}")
    print(f"Top-1 : {metriques.top1:.1%}")
    print(f"Top-3 : {metriques.top3:.1%}")
    print(f"Top-5 : {metriques.top5:.1%}")


if __name__ == "__main__":
    lancer_evaluation_cli()
