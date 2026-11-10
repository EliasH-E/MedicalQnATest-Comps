"""
By: Daya Tucker

Takes a word or phrase that scispacy has pulled from the original text
and standardized possibly. Replaces it with the simplest version from chv

Pulls all terms for the concept ID and 
picks the best replacement via:
    highest combo score -> highest frequency score -> highest context score
"""

import pandas as pd
import spacy
import scispacy
from scispacy.linking import EntityLinker
#from spacy.matcher import PhraseMatcher

special_stop_words = set(["patient"])

def load_chv():
    chv = pd.read_csv(
        "../CHV_words/CHV_concepts_terms_flatfile_20110204.tsv",
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

#print(simplify_term(term, chv))

#Like eventually can do
# for term in scispacy_terms:
   #simple_term = simplify_term(term, chv)

  


def get_medical_phrases(input_text):
    nlp = spacy.load("en_core_sci_md")

    nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    doc = nlp(input_text)

    words = []


    phrase_to_def = {}
    for phrase in doc.ents:
        if phrase._.kb_ents and str(phrase) not in special_stop_words:
            
            #word_list = str(phrase).split(" ")
            words.append(str(phrase))
    return list(words)


def med_simple(input_text):
    med_list = get_medical_phrases(input_text)
    #print(med_list)
    med_dict = {}
    sorted_med_list = sorted(med_list, key=len, reverse=True)
    for i in sorted_med_list:
        simple_term = simplify_term(i,chv)
        
        med_dict[i] = simplify_term(i,chv)
    for i in med_dict:
        input_text = input_text.replace(i,med_dict[i])
    
    new_set = set()
    for i in med_dict:
        split_phrase = med_dict[i].split(" ")
        for word in split_phrase:
            new_set.add(word)
    return [input_text, new_set]



if __name__ == "__main__":
    text = "What causes abetalipoproteinemia? Abetalipoproteinemia is caused by changes (mutations) in the MTTP gene. The MTTP gene gives the body instructions to make a protein needed for creating beta-lipoproteins. These lipoproteins are necessary for the body to absorb fats, cholesterol, and fat-soluble vitamins (vitamins A, D, E and K), and for transporting these substances in the blood. Mutations in the MTTP result in a lack of beta-lipoproteins, leading to an inability to absorb and transport these substances. This in turn leads to the nutritional and neurologic problems in affected people."
    print(med_simple(text))
    