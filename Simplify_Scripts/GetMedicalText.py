import spacy
import scispacy

from scispacy.linking import EntityLinker


def get_medical_phrases(input_text):
    nlp = spacy.load("en_core_sci_md")

    nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    doc = nlp(input_text)

    words = []


    phrase_to_def = {}
    for phrase in doc.ents:
        if phrase._.kb_ents:
            
            word_list = str(phrase).split(" ")
            for i in word_list:
                words.append(i)
    return set(words)
