"""
By: Daya Tucker

Takes a list of tokens (biomedical words) that scispacy has pulled from the original text
and standardized possibly. Replaces all of these with the simplest version.

Should match by longest term first. Pulls all CHV preferred terms for the concept and 
picks the best replacement via:
    highest combo score -> highest frequency score -> highest context score
"""

import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher

def load_chv():
    chv = pd.read_csv(
        "CHV_concepts_terms_flatfile_20110204.tsv",
        sep="\t"
    )

    return chv

chv = load_chv()

def simplify_term(term, chv):
    matches = chv[chv.iloc[:, 1].str.lower() == term.lower()]

    if matches.empty:
        return term

    concept_id = matches.iloc[0, 0]
    concept_terms = chv[chv.iloc[:, 0] == concept_id]
    concept_terms = concept_terms.sort_values(
        by=[
            concept_terms.columns[11], #combo score
            concept_terms.columns[8], #frequency score
            concept_terms.columns[9] #context score
        ],
        ascending=False
    )
    return concept_terms.iloc[0, 1]

term = "hypertension"

print(simplify_term(term, chv))

#Like eventually can do
# for term in scispacy_terms:
   #simple_term = simplify_term(term, chv)