# Tests for determining if we successfully are idntifying nouns to remove
from project1 import nouns


def test_name_removed():
    s = "Alex and Joe went to the store. While there, Jeff bought food for Joe."
    indexes = nouns.mark_names(s)
    assert len(indexes) == 4, "We should have identified 4 names!"
    alex = indexes[0]
    assert s[alex[0]:alex[1]] == 'Alex'
    joe = indexes[1]
    assert s[joe[0]:joe[1]] == 'Joe'
    jeff = indexes[2]
    assert s[jeff[0]:jeff[1]] == 'Jeff'
    joe = indexes[3]
    assert s[joe[0]:joe[1]] == 'Joe'

def test_gender_removed():
    s = "I am She that wrought upon him and her and all others pain!"
    indexes = nouns.mark_genders(s)
    assert len(indexes) == 3


def test_phones():
    s = "Her number was +1(303)555-1111, but I called her at 405.555.1111!"
    indexes = nouns.mark_phones(s)
    assert len(indexes) == 2

def test_dates():
    s = "On Jan 10 of 2018, I will note that 10/15/2018 and 2019.12.24 were days"
    indexes = nouns.mark_dates(s)
    assert len(indexes) == 3
    assert s[indexes[0][0]:indexes[0][1]] == ' Jan 10 of 2018'
    assert s[indexes[1][0]:indexes[1][1]] == '10/15/2018'
    assert s[indexes[2][0]:indexes[2][1]] == '2019.12.24'

def test_addresses():
    s = "I am from Denver, and my place at 123 Blake St. is much nicer" \
        "than my old place at 456 Colfax Ave, Denver CO."
    indexes = nouns.mark_addresses(s)
    assert len(indexes) == 2
    print(indexes)
    # And assert they both work
    assert s[indexes[0][0]:indexes[0][1]] == '123 Blake St.'
    assert s[indexes[1][0]:indexes[1][1]] == '456 Colfax Ave'

