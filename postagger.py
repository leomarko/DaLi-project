# -*- coding: utf-8 -*-
from perceptron import AveragedPerceptron, train as aptrain
import os
import pickle
import codecs
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize



#----------------------------------------------------------------------------------------
class TagPredictor():
    #when instanciating, set ambiguity of tagging.
    #if no loadpath is given, train method needs to be called
    def __init__(self, loadpath=None, ambiguous=False, min_percent=75):
        if loadpath:
            self.apmodel = AveragedPerceptron(loadpath)
        self.amb = ambiguous
        self.min_p = min_percent
            
    def train(self, sentences, tags, nr_iters):
        #the number total number of items in sentences must be equal to number of tags
        features = list()
        for s in sentences:
            f_list = make_featurelist(s)
            features += f_list
        assert len(features) == len(tags)
        examples = list(zip(features,tags))
        self.apmodel = aptrain(nr_iters, examples)

    def predict(self, sentence):
        f_list = make_featurelist(sentence)
        if self.amb:
            tags = [self.apmodel.predict_alternatives(f, min_percent=self.min_p) for f in f_list]
        else:
            tags = [self.apmodel.predict(features) for features in f_list]
        return tags

    def tokenize_tag(self, sentence):
        sentence = word_tokenize(sentence, language='swedish')
        tags = self.predict(sentence)
        return list(zip(sentence, tags))


#----------------------------------------------------------------------------------------------------
#global functions
def _listget(list_,index):
    try:
        return list_[index]
    except(IndexError):
        return None
        
def read_preprocess(file):
    #designed for use with the Stockholm-Umeå Corpus
    #returns a tuple with two lists, one of sentences, the other tags
    #replaces the POS-tag for certain specific forms
    sentences, tags = list(), list()    
    with codecs.open(file, 'r', encoding='utf-8') as f:
        sentence = list()
        for line in f:
            if line == '\n':
                if len(sentence) > 0:
                    sentences.append(sentence)
                sentence = list()
                continue
            data = line.split()
            
            """abbreviations have irregular annotation and are not very relevant
            they are the only words causing irregular feature-separation,
            and are skipped (as they will be False) in the following"""
            if data[3].isupper():
                
                """particular forms of POS that are relevant to this task are given
                special tags instead of their POS tag"""
                if data[3] == 'NN' and data[1].lower()[:-1] != data[2] and 'SMS' in data[5]:
                    #"Sammansättning": Special compound form of noun, ending with '-' in the data
                    data[3] = 'SMS'
                elif data[3] == 'NN' and 'SIN|IND|NOM' in data[5]:
                    #singular indicative nominative noun, usual form for first part of compounds
                    data [3] = 'BASE_N'
                elif data[3] == 'VB' and 'IMP' in data[5]:
                    data[3] = 'IMP_V' #the same form often used in compounds
                    
                sentence.append(data[1]) #the word
                tags.append(data[3]) #the tag
                
    return (sentences, tags)

def make_featurelist(s):
    #Takes a sentence and returns a list with one element per word.
    #Each element is a set of features for that word
    f_list = []
    n = 0
    while n < len(s):
        prv = _listget(s, n-1) #returns None if none
        nxt = _listget(s, n+1) #returns None if none
        features = get_features(s[n], prevw=prv, nextw=nxt)
        f_list.append(features) #adds one set per word
        n += 1
    return f_list

def get_features(word, prevw=None, nextw=None):
    """
    adds all affixes up to 5 characters long, assuming the root is at least 2 characters
    prefixes marked with -p- after
    adds suffixes up to 3 characters long from surrounding words, marked with -prev- and -next-
    the whole word is added as a feature, marked -w- after,
    if the word has a capital initial "-capital-" feature is added.
    returns a set of features
    """
    def _add_features(word, max_length, mark=''):
        if word:
            word = word.lower()
            features.add(mark + word + '-w-')
            for i in range(1, len(word) - 1):
                if i > max_length:
                    break
                if mark == '':
                    features.add(mark + word[:i] + '-p-') #prefix, only added for main word
                features.add(mark + word[-i:]) #suffix

    features = set()            
    if word[0].isupper() and prevw and not word.isupper(): #capital initial
        features.add('-capital-')
    _add_features(word, 5)
    _add_features(prevw, 3, '-prev-')
    _add_features(nextw, 3, '-next-')
    return features


#-------------------------------------------------------------------------------------------
#testing function
def test(training_file, test_file, nr_iters):
    sentences, tags = read_preprocess(training_file)
    tagpredictor = TagPredictor()
    tagpredictor.train(sentences,tags, nr_iters)

    #prediction
    test_sentences, correct_tags = read_preprocess(test_file)
    guesslist = list()
    for s in test_sentences:
        guesses = tagpredictor.predict(s)
        guesslist += guesses
    assert len(guesslist) == len(correct_tags)
    
    #analyzing results
    falsetags = defaultdict(lambda: defaultdict(int))
    right = 0
    for i in range(len(guesslist)):
        if guesslist[i] == correct_tags[i]:
            right += 1
        else:
            falsetags[correct_tags[i]][guesslist[i]] += 1
            
    procent_right = round(right / len(guesslist) * 100, 3)
    
    print("Amount correct: " + str(right) + "\n" +
          "Amount incorrect: " + str(len(guesslist) - right) + "\n" +
          "Accuracy: " + str(procent_right) + "%")
    print('\n\nMispredictions:')
    for tag in falsetags:
        print('\nTag '+tag+' misidentified as:')
        for p in falsetags[tag]:
            print(str(p)+': '+str(falsetags[tag][p])) #str() is used in case label is None
    

#---------------------------------------------------------------------------------
#training and saving a model to use with the tagger
def save_apmodel(training_file,nr_iters,savedir):
    sentences, tags = read_preprocess(training_file)
    tagpredictor = TagPredictor()
    tagpredictor.train(sentences,tags,nr_iters)
    tagpredictor.apmodel.save(savedir)


#---------------------------------------------------------------------------------
def main():
    training = "suc-train.conll"
    testing = "suc-test.conll"
    savedir = 'apmodel.p'
    mode = int(input('Train and test, or train and save? Input 1 or 2\n'))
    nr_iters = int(input('Number of iterations for training:\n'))
    if mode == 1:
        test(training, testing, nr_iters)
    elif mode == 2:
        savedir = 'apmodel_' + input('version name:\n') + '.p'
        save_apmodel(training, nr_iters, savedir)
        print('Saved')

if __name__ == '__main__':
    main()
