# CS 5293 Project 1 Jordan Crawford

## Overview

This is a tool designed to flexibly obfuscate files on a variety of parameters,
with the ability both to exclude specific bits of information, like dates,
names, or phone numbers, as well as to block whole-sale information about broad
concepts. 

## Usage

To run the program, execute:
```bash
pipenv run python -m project1.main [-h] --input INPUT [--output OUTPUT]
    [--stats STATS] [--names] [--genders] [--dates] [--addresses] [--phones]
    [--concept CONCEPT]
```
INPUT is specified as a glob of files, and the `--input` flag can be specified
multiple times to supply multiple globs. 

OUTPUT is a directory where redacted files will be stored (defaulting to the
current working directory)

STATS is the file that statistics information should be written to. By default
this information is written to standard out.

All of `[--names]` `[--genders]` `[--dates]` `[--addresses]` and 
`[--phones]` simply specify that you wish to obfuscate those fields.
In particular, these fields are detected as follows:
* Names are detected using NLTK's default named entity recognition, 
  looking for the 'PERSON' type. 
* Genders specifies the 6 words 'she', 'her', 'hers', 'he', 'him', 
  and 'his'
* Dates are anything that vaguely look like dates. In particular, 
  this program scans for two things. First, dates that are a month, written out
  as 'Feb' or 'February', and any near by numbers that may be years or days.
  Second, it looks for patterns of numbers like '5/15' or '5/25/2013' (etc.),
  which may be years. All of this is implemented via two regexes. 
* Addresses are detected by using Google's Natural Language
  Processing API. In particular, everything that has a number in it and which
  is recognized as a 'LOCATION' by that API is obfuscated by this flat. For
  example, 'Denver' would not be obfuscated on its own, but '123 E. Grant St.'
  would be. 
* Phone numbers are detected via a regex that searches for the
  correct numbers of digits delimited by just about anything (or in fact,
  nothing). The hope is that this is flexible enough to capture just about any
  way that someone might chose to write a phone number. 

CONCEPT, just like input, can be specified multiple times by simply repeating
the `--concept` flag. A sentence is obfuscated if it matches any of these
concepts. Specifically, we take the incoming concept and look for all synonyms
as well as all words that are, in NLP speak, 'hyponyms' - basically, words that
are instances of broader concepts.  Once we have this full set of words
populated, we simply scan each sentence in the document(s) specified; if the
sentence has that word in it (or a derivation), we obfuscate that sentence.
This means that, when you specify a concept like 'animals', sentences about
bacteria will not be censored (they are about a similar and related concept,
but bacteria are not animals), but a sentence that mentions 'dog' or 'cat' will
be censored, since dogs and cats are both animals. 

## Example Stats File

This is an example statistics file. The structure is largely self
explanatory: The first section gives details about the total number
of times that we encountered any given type of obfuscation. After that,
the same output is repeated, but broken out with per-file statistics. 
```
Obfuscation stats
Overall stats:
	names: 6
	genders: 4
	dates: 4
	addresses: 2
	phones: 2
For file temp/input2.txt
	names: 3
	genders: 2
	dates: 2
	addresses: 1
	phones: 1
For file temp/input1.txt
	names: 3
	genders: 2
	dates: 2
	addresses: 1
	phones: 1
```

## Tests

To run tests execute:
```
pipenv run python setup.py test
```
This prints the test result (generated via pytest) to standard out. 
