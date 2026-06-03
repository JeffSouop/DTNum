# Assistant Fiscal DGFiP

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer L'Interface

```bash
streamlit run app.py
```

## Lancer L'Évaluation

Depuis l'environnement virtuel activé :

```bash
python -m src.evaluate
```

## Structure Du Projet

```text
.
├── app.py
├── data/
│   ├── info_particulier_impot.csv
│   └── questions_fiches_fip.csv
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── evaluate.py
│   └── retrieval.py
├── requirements.txt
└── README.md
```
