
# By Daya Tucker
# Part-of-speech tagger and dependency parser.

#
# Outputs pipe delimited tokens to be passed to Java SimpleNLG.

import spacy

nlp = spacy.load("en_core_web_sm")

#example input text:
text = "the fox jumps and slides over the lazy dog."


def analyze_sentence(text):
    doc = nlp(text)
    tokens = []

    for token in doc:
        if not token.is_space:
            tokens.append(
                f"{token.text}|{token.pos_}|{token.lemma_}|"
                f"{token.dep_}|{token.head.text}|{token.head.pos_}"
            )
    return "\n".join(tokens)

if __name__ == "__main__":
    result = analyze_sentence(text)
    print(result)
