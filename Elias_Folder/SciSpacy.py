import spacy
import scispacy

from scispacy.linking import EntityLinker

nlp = spacy.load("en_core_sci_md")

# This line takes a while, because we have to download ~1GB of data
# and load a large JSON file (the knowledge base). Be patient!
# Thankfully it should be faster after the first time you use it, because
# the downloads are cached.
# NOTE: The resolve_abbreviations parameter is optional, and requires that
# the AbbreviationDetector pipe has already been added to the pipeline. Adding
# the AbbreviationDetector pipe and setting resolve_abbreviations to True means
# that linking will only be performed on the long form of abbreviations.
nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})

text = "Stuart has muscular atrophy that may be linked to his cancer diagnosis"
doc = nlp(text)

print(doc.ents)
# Let's look at a random entity!
entity = doc.ents[-1]

print("Name: ", entity)


linker = nlp.get_pipe("scispacy_linker")
phrase_to_def = {}
for phrase in doc.ents:
    if phrase._.kb_ents:
        
        definition = linker.kb.cui_to_entity[phrase._.kb_ents[0][0]].definition
        if(not definition):
            continue
        definition = definition[:-1]
        phrase_to_def[phrase] = definition
      

for i in phrase_to_def:
    new_phrase = str(i) + ", " + str(phrase_to_def[i]).lower()

    text = text.replace(str(i), str(i) + ", the " + str(phrase_to_def[i]).lower())
print(text)