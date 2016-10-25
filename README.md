Samsacheck – a compound error checker for swedish

Python

Author: Leo Marko Englund

Project in computational linguistics at Stockholm University fall 2016


This program is designed to detect incorrectly separated compound words

in swedish (särskrivning). It takes as input a text file and outputs the line

numbers and words that are suspected to be misspelled compounds.

samsacheck_pdf.py accepts pdf files as input, but it is still in early 

development and doesn't give good results.


Dependencies: 

NLTK

NLTK Punkt tokenizer trained for swedish (available in NLTK data)

PyPDF2 (only for samsacheck_pdf)



Samsacheck features a part-of-speech tagger built on machine learning

using a Perceptron algorithm. The tagger is customized for the task of 

compound detection and built to work with the Stockholm-Umeå Corpus 

(SUC). The accuracy of tagging is around 95.5%.  A pre-trained model 

(apmodel_suc3iter.p) is freely available to use. Using the postagger.py is

not recommended unless you have access to SUC, and it should be noted

that it preprocesses the tags so they are no longer pure part-of-speech tags.



Ambiguity calibration

A notable command line option for samsacheck is -p or –minpercent, 

which sets the ”unambiguity level” for POS-tags. Rather than giving one

tag per word, the tagger for Samsacheck by default gives a word a set of

tags, and the unambiguity levels specifies how high the score of accepted

tags must be in percent of the top scoring tag. 

For example, a word may be tagged as a noun but also having many 

features implying it being a proper name, the default unambiguity level of

75% might give the word both tags, 99% or unambiguous tagging would 

only give the tag noun, and a very low unambiguity would likely include all

sorts of tags.

Some ambiguity is recommended for the compound pattern detection to 

work well. The unambiguity can be set for each program run, and defaults

to 75 (percent).
