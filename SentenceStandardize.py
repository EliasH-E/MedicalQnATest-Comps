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
#reads as tsv with no column names
chv = pd.read_csv("CHV_words/CHV_concepts_terms_flatfile_20110204.tsv", sep="\t", header=None)
print(chv.columns.tolist())
print(chv.head())
chv = chv.rename(columns={0: "CUI", 1: "term", 2: "clinicalTerm", 3: "CHVTerm"})
results = chv[
    chv["term"].str.contains("vitamin b3", case=False, na=False)
]

print(
    results[
        ["CUI", "term", "clinicalTerm", "CHVTerm"]
    ]
)
#for testing. can replace with user input
sentence = "Do I have a heart attack or high blood pressure"
tokens = word_tokenize(sentence.lower())
newTok = []

i = 0

while i < len(tokens):
    matched = False

    for length in range(4, 0, -1):
        if i + length <= len(tokens):
            term = " ".join(tokens[i:i + length])

            match = chv["term"].str.lower() == term
            matches = chv[match]
            if not matches.empty:
                clinical = matches.iloc[0]["clinicalTerm"]

                newTok.append(clinical)

                i += length
                matched = True
                break

    if not matched:
        newTok.append(tokens[i])
        i += 1
#will be in lowercase. lowercase dataset?
sentence = " ".join(newTok)

print(sentence)