#importer
from perceptron2 import AveragedPerceptron, train as aptrain
from compoundabilitydict import CompableDict #, word_to_tag_dict
import os
import pickle
import re
# -*- coding: utf-8 -*-

"""
notes:
Fix unicode decoding problem
"""

#----------------------------------------------------------------------------------------
class TagPredictor():
    def __init__(self, loadpath=None):
        if loadpath:
            self.apmodel = AveragedPerceptron(loadpath)
            
    def train(self, sentences, tags, nr_iters):
        #the number total number of items in sentences must be equal to number of tags
        def _train(sentences,tags,nr_iters,repeat=False):
            features = list()
            for s in sentences:
                f_list = self.make_featuresets(s,repeat)
                features += f_list
            assert len(features) == len(tags)
            examples = list(zip(features,tags))
            self.apmodel = aptrain(nr_iters, examples)
        _train(sentences,tags,nr_iters)
        _train(sentences,tags,nr_iters,repeat=True)

    def make_featuresets(self, s, repeat=False):
    #Takes a sentence and returns a list with one element per word.
    #Each element is a set of features for that word
        f_list = []
        n = 0
        prevtags = [None,None]
        while n < len(s):
            prv = _listget(s, n-1) #returns None if none
            nxt = _listget(s, n+1) #returns None if none
            features = self.get_features(s[n], prevw=prv, nextw=nxt, prevtags=prevtags)
            f_list.append(features) #adds one set per word
            if n > 1:
                prevtags[1] = prevtags[0]
            if n > 0 and repeat:
                prevtags[0] = self.predict(f_list[-1],sentence=False)
            n += 1
        return f_list

    def get_features(self, word, prevw=None, nextw=None, prevtags=[]):
        """
        adds all affixes up to 5 characters long, assuming the root is at least 2 characters
        prefixes marked with -p- after
        adds suffixes up to 3 characters long from surrounding words, marked with -prev- and -next-
        adds the whole word is added as a feature marked -w-
        adds the correct/predicted tags for the 2 previous words (test also with predicted only)
        returns a set of features
        """
        def _add_features(word, max_length, mark=''):
            features.add(mark + word + '-w-')
            for i in range(1, len(word) - 1):
                if i > max_length:
                    break
                if mark == '':
                    features.add(mark + word[:i] + '-p-') #prefix, only added for main word
                features.add(mark + word[-i:] + '-s-') #suffix
                    
        features = set()
        _add_features(word, 5)
        if prevw:
            _add_features(prevw, 3, '-prev-')
        else:
            features.add('-first-')
        if nextw:
            _add_features(nextw, 3, '-next-')
        else:
            features.add('-last-')
        for i in range(len(prevtags)):
            if prevtags[i]:
                features.add(prevtags[i] + '-p'+str(i)+'t-')
            
        return features

    def predict(self, featuresets, sentence=True):
        if sentence:
            return [self.apmodel.predict(features) for features in featuresets]
        else:
            return self.apmodel.predict(featuresets)

    def tokenize_tag(self, string):
        sentence = string.split()
        toanalyze = string.lower().split()
        tags = self.predict(self.make_featuresets(toanalyze))
        return list(zip(sentence, tags))


#----------------------------------------------------------------------------------------------------
#globala funktioner
def _listget(list_,index):
    try:
        return list_[index]
    except(IndexError):
        return None
        
def read_data(file):
    #returns a tuple with two lists, one of sentences, the other tags
    sentences, tags = list(), list()    
    with open(file, 'r') as f:
        #word and POS-tag is the 2nd and 4th token of each line in this data
        sentence = list()
        for line in f:
            if line == '\n':
                if len(sentence) > 0:
                    sentences.append(sentence)
                sentence = list()
                continue
            data = line.split()[1:4:2]
            sentence.append(data[0])
            tags.append(data[1])
    return (sentences, tags)


#-------------------------------------------------------------------------------------------
#testing function
def test(training_file, test_file, nr_iters):
    sentences, tags = read_data(training_file)
    tagpredictor = TagPredictor()
    tagpredictor.train(sentences,tags, nr_iters)

    #prediction
    test_sentences, correct_tags = read_data(test_file)
    guesslist = list()
    for s in test_sentences:
        s = tagpredictor.make_featuresets(s)
        guesses = tagpredictor.predict(s)
        guesslist += guesses
    assert len(guesslist) == len(correct_tags)
    
    right = 0
    for i in range(len(guesslist)):
        if guesslist[i] == correct_tags[i]:
            right += 1
            
    procent_right = round(right / len(guesslist) * 100, 3)
    
    print("Amount correct: " + str(right) + "\n" +
          "Amount incorrect: " + str(len(guesslist) - right) + "\n" +
          "Accuracy: " + str(procent_right) + "%")

#---------------------------------------------------------------------------------
#training and saving a model to use with the tagger
def save_apmodel(training_file,savedir, nr_iters):
    sentences, tags = read_data(training_file)
    tagpredictor = TagPredictor()
    tagpredictor.train(sentences,tags,nr_iters)
    tagpredictor.apmodel.save(savedir)


#---------------------------------------------------------------------------------
def main():
    #training = os.curdir+"\sv-universal-train.conll"
    #testing = os.curdir+"\sv-universal-test.conll"
    training = os.curdir+"\suc-train.conll"
    testing = os.curdir+"\suc-dev.conll"
    savedir = 'apmodel.p'
    mode = int(input('Train and test, train and save, or check compundability?\n Input 1, 2 or 3\n'))
    nr_iters = int(input('Number of iterations for training:\n'))
    if mode == 1:
        test(training, testing, nr_iters)
    elif mode == 2:
        savedir = 'apmodel_' + input('version name:\n') + '.p'
        save_apmodel(training, savedir, nr_iters)
        print('Saved')
        
    #Not working yet:
    elif mode == 3:
        sentences, tags = read_data(training)
        tagpredictor = TagPredictor()
        features = dict()
        for s in sentences:
            flist = tagpredictor.make_featuresets(s)
            featurelist = list()
            for fset in flist:
                for f in fset:
                    featurelist.append(f)
            for f in featurelist:
                if f in features:
                    features[f] += 1
                else:
                    features[f] = 1
        print(features)
        cpb = CompableDict(features)
        cpb.show()
        

if __name__ == '__main__':
    main()
