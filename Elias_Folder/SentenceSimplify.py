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
import copy

from sentence_transformers import SentenceTransformer



#nltk.download('punkt_tab')
#nltk.download('book_grammars')
#nltk.download('averaged_perceptron_tagger_eng')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
stop_words = set(stopwords.words('english'))
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


def compare(embeds, sent2, model):
    
    sentences = [sent2]
    embeddings = model.encode(sentences)
    return model.similarity(embeds, embeddings[0])

def simplify_total_sentence(sentence, imporant_words):
    #print(sentence)
   
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    
    current_sentence = tokens.copy()
    

    new_words = []
    id = 0
    for word, tag in tagged:
        wn_pos = to_wordnet_pos(tag)

        # leave punctuation, stopwords, etc. alone
        if wn_pos is None or not word.isalpha() or word in imporant_words or word in stop_words:
            new_words.append(word)
            id += 1
            continue

        lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)

        my_syns = {lemma: avg_zipf(lemma)}
        for syn in wordnet.synsets(lemma, pos=wn_pos):
            for related in [syn][:15] + syn.hyponyms()[:15] + syn.hypernyms()[:15]:
                for lem in related.lemmas():
                    #print(lem.name())
                    my_syns[lem.name()] = avg_zipf(lem.name())

        sorted_syns = dict(sorted(my_syns.items(), key=lambda item: item[1], reverse=True))
        #best_word = None
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        orig_embed = model.encode(" ".join(current_sentence))
        for i in sorted_syns:
            current_copy = current_sentence.copy()
            current_copy[id] = " ".join(i.split("_"))
            comp_score = compare(orig_embed," ".join(current_copy), model)
            if(comp_score >= 0.9):
                best_word = i
                break
            my_syns[i] = my_syns[i]*comp_score
        
        best_word = max(my_syns, key=my_syns.get)
        new_words.extend(best_word.split("_"))
        current_sentence[id] = " ".join(best_word.split("_"))
        id += 1
        #print(current_sentence)

    new_sentece = ""
    for i in range(len(new_words)):
        if(i != 0 and new_words[i][0].isalpha()):
            new_sentece += " "
        new_sentece += new_words[i]
    
    sentence = new_sentece
    return new_sentece

#print(simplify_total_sentence("dog barked at the man",set([])))