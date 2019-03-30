# All of the function associated with redacting
# any user-specified concept. This suplies a single
# public function, which accepts a sentnce and a
# concept, and returns a boolean to indicate if it
# should be redacted. 

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from  nltk.corpus import stopwords 
import nltk

wml = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# A concept is created by taking the concept
# and determining it's closure in terms of 
# words.

def gen_concept_map(concept):
    senses = wn.synsets(concept)
    sub_concepts = {
        lemma.name()
        for sense in senses
        for child_sense in sense.closure(lambda s: s.hyponyms())
        for lemma in child_sense.lemmas()
    }
    sub_concepts.add(concept)
    # This returns the list of words we block
    return sub_concepts

# We then look for all of those words, and reject
# a sentence if it has one. 
def matches_concept(sentence, concept_map):
    words = nltk.word_tokenize(sentence)
    real_words = [
        wml.lemmatize(word)
        for word in words
        if not word in stop_words
    ]
    for word in real_words:
        if word in concept_map:
            return True
    return False

def mark_concept_sentences(text, concept):
    concept_map = gen_concept_map(concept)
    i = 0
    sents = nltk.sent_tokenize(text)
    output = []
    for sent in sents:
        if matches_concept(sent, concept_map):
            i = text.index(sent, i)
            output.append((i, i + len(sent)))
            i += len(sent)
    return output

