# Code for redacting nouns. Specifically, implements logic for taking a
# block of text and returning the indexes of words that match any of the following:
#  - names      All words nltk tags as PERSON
#  - genders    Regex for he, him, his, she, her, hers
#  - dates      ????
#  - addresses  ????
#  - phones     Regex

# Each takes a sentence as input and outputs a list of indexes that should
# be redacted.

import nltk
import re

from google.cloud import language
from google.cloud.language import enums, types


def mark_names(text):
    sentences = nltk.sent_tokenize(text)
    name_indexes = []
    i = 0
    for s in sentences:
        words = nltk.word_tokenize(s)
        tags = nltk.pos_tag(words)
        chunked = nltk.ne_chunk(tags)
        for chunk in chunked:
            if not (hasattr(chunk, 'label') and chunk.label() == 'PERSON'):
                continue
            # We've got ourselves a person!
            for word in chunk:
                remove_from = text.index(word[0], i)
                name_indexes.append(
                    (remove_from, remove_from + len(word[0]))
                )
        i += len(s) + 1
    return name_indexes

GENDER_REGEX = re.compile(r'she|her|hers|he|him|his', re.IGNORECASE)

def mark_genders(text):
    # Simple regex search
    words = nltk.word_tokenize(text)
    gender_indexes = []
    i = 0
    for word in words:
        if GENDER_REGEX.match(word):
            remove_from = text.index(word)
            i = remove_from + len(word)
            gender_indexes.append(
                (remove_from, i)
            )
    return gender_indexes


# Create a client to interface with Google Cloud NLP to find
# addresses
client = language.LanguageServiceClient()
DIGIT_REGEX = re.compile(r'\d+')

def mark_addresses(text):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT
    )
    resp = client.analyze_entities(
        document=document, 
        encoding_type='UTF32',
    )
    return [
        (m.text.begin_offset, m.text.begin_offset + len(m.text.content))
        for e in resp.entities
        for m in e.mentions
        if e.type == enums.Entity.Type.LOCATION \
            and DIGIT_REGEX.search( m.text.content )
    ]


MONTHS_REGEX_TEXT = r'(\d+.{0,8})?\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)[\.\,\-\s](.{0,8}\d+)?'
MONTHS_REGEX = re.compile(MONTHS_REGEX_TEXT, re.IGNORECASE)

def _mark_month_dates(text):
    return [(m.start(0), m.end(0)) for m in re.finditer(MONTHS_REGEX, text)]   

# This is a bit gnarly...
DATE_REGEX = re.compile(r'(?<!\d)(\d{4}|\d{1,2})[\s/\-\.](\d{4}|\d{1,2})([\s/\-\.](\d{4}|\d{1,2}))?(?!\d)')

def _mark_number_dates(text):
    return [(m.start(0), m.end(0)) for m in re.finditer(DATE_REGEX, text)]   

def mark_dates(text):
    return _mark_month_dates(text) + _mark_number_dates(text)

PHONENUM_REGEX = re.compile(r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}')

def mark_phones(text):
    # Simple regex search - don't tokenize to avoid splitting number across
    # multiple words    
    return [(m.start(0), m.end(0)) for m in re.finditer(PHONENUM_REGEX, text)]   
