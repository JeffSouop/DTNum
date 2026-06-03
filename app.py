from __future__ import annotations

import streamlit as st

from src.retrieval import MoteurRechercheFiches, ResultatRecherche

st.set_page_config(
    page_title="Assistant fiscal DGFiP",
    layout="wide",
)

st.title("Assistant fiscal — recherche de fiche pratique")
st.caption(
    "Posez une question fiscale : le système propose les fiches pratiques "
    "les plus pertinentes issues de l'espace particulier impots.gouv."
)


@st.cache_resource(show_spinner="Construction de l'index TF-IDF des fiches…")
def obtenir_moteur_recherche() -> MoteurRechercheFiches:
    return MoteurRechercheFiches()


def afficher_fiche_recommandee(resultat: ResultatRecherche) -> None:
    st.markdown(f"### {resultat.titre}")
    st.write(resultat.extrait)
    if resultat.url:
        st.markdown(f"[Ouvrir la fiche sur impots.gouv]({resultat.url})")


nombre_resultats = 1

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["contenu"])

question = st.chat_input("Posez votre question fiscale")

if question and question.strip():
    question = question.strip()
    st.session_state.messages.append({"role": "user", "contenu": question})
    with st.chat_message("user"):
        st.markdown(question)

    moteur = obtenir_moteur_recherche()
    resultats = moteur.rechercher(question, nombre_resultats=nombre_resultats)

    with st.chat_message("assistant"):
        if not resultats:
            contenu_reponse = "Aucune fiche pratique pertinente n'a été trouvée."
            st.warning(contenu_reponse)
        else:
            resultat = resultats[0]
            contenu_reponse = (
                f"### {resultat.titre}\n\n"
                f"{resultat.extrait}\n\n"
                f"[Ouvrir la fiche sur impots.gouv]({resultat.url})"
            )
            afficher_fiche_recommandee(resultat)

    st.session_state.messages.append(
        {"role": "assistant", "contenu": contenu_reponse}
    )
