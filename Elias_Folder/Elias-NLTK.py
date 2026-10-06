import nltk
from nltk import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.text import Text
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

lemmatizer = WordNetLemmatizer()

nltk.download('punkt_tab')
nltk.download('book_grammars')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
nltk.download('omw-1.4')
text = "Hello World! There are lots of things that you can do with NLTK, I found some pretty cool features! But before I forget, I should mention that I am going to be studying some more in the future."
print("Input Text: ")
text = text.lower()
print(text)

sample_text = Text(text)


#This tokenizes(splits up) the text

words = word_tokenize(text)
print("Tokenized Text:")
print(words)

tagged_words = nltk.pos_tag(words)
print("TaggedText:")
print(tagged_words)
print(words)


#This is all of the stop words in english, stop words are useless words for analysis like 'with' and 'and'
stop_words = set(stopwords.words('english'))

#Removes stop words from text
cleaned_words = [word for word in words if word.lower() not in stop_words and word.isalnum()]

print("Cleaned Text:")
print(cleaned_words)

#Lemmitizes(?) the text
#lemmized_words = 

#Gets the frequency of words used, important for text complexity
word_frequencies = FreqDist(cleaned_words)

print("Word Frequency of Cleaned Text:")
for word, frequency in word_frequencies.items():
    print(f"{word}: {frequency}")

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('V'):
        return 'v'
    elif tag.startswith('N'):
        return 'n'
    elif tag.startswith('R'):
        return 'r'
    else:
        return 'n'
lemmatized_sentence = []
for word, tag in tagged_words:
    if word.lower() == 'are' or word.lower() in ['is', 'am']:
        lemmatized_sentence.append(word)
    else:
        lemmatized_sentence.append(
            lemmatizer.lemmatize(word, get_wordnet_pos(tag)))

print("This is a lemmatized sentence")
print(" ".join(lemmatized_sentence))

stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in words]
print("This is a stemmed sentence")
print(" ".join(stemmed_words))

atrophies = wordnet.synsets('atrophy')
for i in atrophies:
    print(i.lemmas())

#dt = nltk.DiscourseTester(['A student dances', 'Every student is a person'])
#print(dt.readings())