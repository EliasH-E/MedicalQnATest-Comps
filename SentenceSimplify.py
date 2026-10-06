import nltk
from nltk import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.text import Text
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import wordfreq


#nltk.download('punkt_tab')
#nltk.download('book_grammars')
#nltk.download('averaged_perceptron_tagger_eng')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

def to_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    if tag.startswith("V"):
        return wordnet.VERB
    if tag.startswith("N"):
        return wordnet.NOUN
    if tag.startswith("R"):
        return wordnet.ADV
    return None  # determiners, prepositions, etc.

def avg_zipf(name):
    parts = name.split("_")
    total_freq = 2
    for i in parts:
        total_freq += wordfreq.zipf_frequency(i, "en") - 2
    return total_freq / len(parts)


sentence = "The diminutive feline procured a morsel of loaves. The beguiled fellow of a corrupted disposition devises a plan of misfortune and misery"
#sentence = "Adult acute myeloid leukemia (AML) is a type of cancer in which the bone marrow makes abnormal myeloblasts (a type of white blood cell), red blood cells, or platelets."
#sentence = "Henry went to the store"
print(sentence)
for i in range(1):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    new_words = []
    for word, tag in tagged:
        wn_pos = to_wordnet_pos(tag)

        # leave punctuation, stopwords, etc. alone
        if wn_pos is None or not word.isalpha():
            new_words.append(word)
            continue

        lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)

        my_syns = {lemma: avg_zipf(lemma)}
        for syn in wordnet.synsets(lemma, pos=wn_pos):
            for related in [syn] + syn.hyponyms() + syn.hypernyms():
                for lem in related.lemmas():
                    my_syns[lem.name()] = avg_zipf(lem.name())

        best_word = max(my_syns, key=my_syns.get)
        new_words.extend(best_word.split("_"))

    new_sentece = ""
    for i in range(len(new_words)):
        if(i != 0 and new_words[i][0].isalpha()):
            new_sentece += " "
        new_sentece += new_words[i]
    print(new_sentece)
    sentence = new_sentece