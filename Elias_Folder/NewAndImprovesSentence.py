import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.wsd import lesk
from nltk.corpus import stopwords
import wordfreq
import lemminflect
from lemminflect import getInflection
import spacy

from sentence_transformers import SentenceTransformer
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

INCLUDE_HYPONYMS = True  
MAX_SENSE_RANK = 15      # candidate must use this sense as one of ITS top N senses



def compare(embeds, sent2, model):
    
    sentences = [sent2]
    embeddings = model.encode(sentences)
    return model.similarity(embeds, embeddings[0])


def to_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    if tag.startswith("V"):
        return wordnet.VERB
    if tag.startswith("N"):
        return wordnet.NOUN
    if tag.startswith("R"):
        return wordnet.ADV
    return None


def fix_pos(lemma, wn_pos):
    """
    The POS tagger guesses badly on rare words.
    If WordNet has nothing for the tagged POS, tries everything else
    """
    if wordnet.synsets(lemma, pos=wn_pos):
        return wn_pos
    for other in (wordnet.ADJ, wordnet.NOUN, wordnet.VERB, wordnet.ADV):
        if other != wn_pos and wordnet.synsets(lemma, pos=other):
            return other
    return wn_pos


def avg_zipf(name):
    parts = name.split("_")
    total_freq = 2
    for i in parts:
        total_freq += wordfreq.zipf_frequency(i, "en") - 2
    return total_freq / len(parts)


def pick_sense(tokens, lemma, wn_pos):

    senses = wordnet.synsets(lemma, pos=wn_pos)
    return senses

def inflect_word(name, tag):
    """
    name: name of word
    tag:  original tag (NNS, VBD, VBG, JJR, ...)
    """
    parts = name.split("_")
    # Verbs inflect on the first word (give up -> gave up)
    # others on the last (ice cream -> ice creams)
    i = len(parts) - 1 
    if tag.startswith("V"):
        i = 0 

    forms = getInflection(parts[i], tag=tag) 
    if forms:
        parts[i] = forms[0]
    return parts


def match_case(original, words):
    words = words.copy()
    if len(original) > 1 and original.isupper():
        return [w.upper() for w in words]
    if original[0].isupper():
        words[0] = words[0].capitalize()
    return words

def candidate_words(sense, wn_pos):

    found = {}
   # print(sense)
    for syn in sense:
       # print(syn)
        synlist = [syn][:MAX_SENSE_RANK]
        if(INCLUDE_HYPONYMS):
            synlist += syn.hyponyms()[:6] + syn.hypernyms()[:6]
        for related in synlist:
            for lem in related.lemmas():
                name = lem.name()
               # print(name)
                if name != name.lower():
                    continue  # skip proper names
               
              
                found[name] = avg_zipf(name)
                #print(name, found[name])
    return found


#sentence = "The canine barked at the wyvern and the dog"

#print(sentence)
def simplify_total_sentence(sentence, imporant_words):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    new_words = []
    id = 0
    current_sentence = tokens.copy()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    for word, tag in tagged:
        wn_pos = to_wordnet_pos(tag)

        # leave punctuation, stopwords, etc. alone
        if wn_pos is None or not word.isalpha() or word in stop_words or word in imporant_words:
            new_words.append(word)
            continue
        
        if(avg_zipf(word) > 4.5):
            new_words.append(word)
            continue
        lemma = lemmatizer.lemmatize(word.lower(), pos=wn_pos)
        wn_pos = fix_pos(lemma, wn_pos)

        sense = pick_sense(tokens, lemma, wn_pos)
        if sense is None:
            new_words.append(word)
            id += 1
            continue

        my_syns = {lemma: avg_zipf(lemma)}
        my_syns.update(candidate_words(sense, wn_pos))


        sorted_syns = dict(sorted(my_syns.items(), key=lambda item: item[1], reverse=True))
        
        word_to_proper_case = {}
        orig_embed = model.encode(" ".join(current_sentence))
        for i in sorted_syns:
            if(my_syns[i]==0):
               word_to_proper_case[i]=[i]
               continue
            current_copy = current_sentence.copy()
            word_to_proper_case[i] = match_case(word, inflect_word(i, tag)) 
            current_copy[id] = " ".join(word_to_proper_case[i])               
            comp_score = compare(orig_embed," ".join(current_copy), model)
           
            my_syns[i] = my_syns[i]*comp_score*comp_score*comp_score*comp_score*comp_score*comp_score*comp_score*comp_score
       
       
        best_word = max(my_syns, key=my_syns.get)
        new_words.extend(word_to_proper_case[best_word])                 
        
        id += 1

    new_sentence = ""
    for j in range(len(new_words)):
        if j != 0 and new_words[j][0].isalpha():
            new_sentence += " "
        new_sentence += new_words[j]

    sentence = new_sentence
    return new_sentence

#print("Final:",simplify_total_sentence("the man declares his desires", set([])))