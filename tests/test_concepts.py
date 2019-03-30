from project1 import concepts

concept = concepts.gen_concept_map('dog')

def test_basic():
    sentence = "The dog is huge"
    matches = concepts.matches_concept(sentence, concept)
    assert matches

def test_syn():
    sentence = "The hound is huge"
    matches = concepts.matches_concept(sentence, concept)
    assert matches

def test_type():
    sentence = "The terrier is huge"
    matches = concepts.matches_concept(sentence, concept)
    assert matches
    
def test_not():
    sentence = "The cat is huge"
    matches = concepts.matches_concept(sentence, concept)
    assert not matches
