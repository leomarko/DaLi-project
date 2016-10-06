#importer
from perceptron2 import train as aptrain
import os
import time
# -*- coding: utf-8 -*-


#----------------------------------------------------------------------------------------
class TagPredictor():
    def __init__(self, sentences, tags):
        #the number total number of items in sentences must be equal to number of tags
        features = list()
        for s in sentences:
            f_list = make_featurelist(s)
            features += f_list
        assert len(features) == len(tags)
        examples = list(zip(features,tags))
        self.apmodel = aptrain(5, examples)

    def predict(self, sentence):
        f_list = make_featurelist(sentence)
        tags = [self.apmodel.predict(features) for features in f_list]
        return tags


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
        #ord och ordklass tas fram från varje rad, vilket är 2a respektive 4e elementet:
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
    if the word is 2 characters or less, the whole word is added as a feature (instead of affixes)
    this feature is marked -w- after
    returns a set of features
    """
    def _add_features(word, max_length, mark=''):
        if word:
            if len(word) < 3:
                features.add(mark + word + '-w-')
                return
            for i in range(1, len(word) - 1):
                if i > max_length:
                    break
                if mark == '':
                    features.add(mark + word[:i] + '-p-') #prefix, only added for main word
                features.add(mark + word[-i:]) #suffix
                
    features = set()
    _add_features(word, 5)
    _add_features(prevw, 3, '-prev-')
    _add_features(nextw, 3, '-next-')
    return features


#-------------------------------------------------------------------------------------------
#testing function
def test(training_file, test_file):
    sentences, tags = read_data(training_file)
    tagpredictor = TagPredictor(sentences,tags)

    #prediction
    test_sentences, correct_tags = read_data(test_file)
    guesslist = list()
    for s in test_sentences:
        guesses = tagpredictor.predict(s)
        guesslist += guesses
    assert len(guesslist) == len(correct_tags)
    
    #här stäms det av hur många taggar blev korrekta och skriver ut resultaten för det
    right = 0
    for i in range(len(guesslist)):
        if guesslist[i] == correct_tags[i]:
            right += 1
            
    procent_right = round(right / len(guesslist) * 100, 3)
    
    print("Amount correct: " + str(right) + "\n" +
          "Amount incorrect: " + str(len(guesslist) - right) + "\n" +
          "Accuracy: " + str(procent_right) + "%")

#testkörning (svenska)
if __name__ == '__main__':
    training = os.curdir+"\sv-universal-train.conll"
    testing = os.curdir+"\sv-universal-test.conll"
    start_time = time.clock()
    test(training, testing)
    print("\n%s seconds" % (time.clock() - start_time))