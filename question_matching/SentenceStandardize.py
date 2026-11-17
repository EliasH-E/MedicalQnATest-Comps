import nltk
from nltk import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.util import ngrams
from nltk.probability import FreqDist
from nltk.text import Text
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pandas as pd 
""" Loads the Consumer Health Vocabulary (CHV) dataset as a TSV file
    Columns are, from left to right, concept id, consumer terms, and clinical terms 
"""
chv = pd.read_csv("CHV_concepts_terms_flatfile_20110204.tsv", sep="\t", header=None, low_memory=False)
chv = chv.rename(columns={0: "CUI", 1: "term", 2: "clinicalTerm", 3: "CHVTerm"})

""" Takes in user input sentence and replaces consumer terms with clinical terms from CHV dataset. 
    Returns the new sentence in lowercase.
"""
def standardize(sentence):
    tokens = word_tokenize(sentence.lower())
    newTok = []
    i = 0

    while i < len(tokens):
        matched = False
        # Searches for consumer terms, starting from 4 token phrases down to 1 token
        for length in range(4, 0, -1):
            if i + length <= len(tokens):
                term = " ".join(tokens[i:i + length])
                match = chv["term"].str.lower() == term
                matches = chv[match]
                # Replace matched phrases
                if not matches.empty:
                    clinical = matches.iloc[0]["clinicalTerm"]
                    newTok.append(clinical)
                    i += length
                    matched = True
                    break
        # Keep original tokens
        if not matched:
            newTok.append(tokens[i])
            i += 1
    sentence = " ".join(newTok)
    return sentence