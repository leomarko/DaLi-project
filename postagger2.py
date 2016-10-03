#importer
from perceptron2 import train
import os
# -*- coding: utf-8 -*-


#----------------------------------------------------------------------------------------
# klassen TagPredictor med sina funktioner nedan
class TagPredictor():
    def __init__(self, tupler):


        
        ordlista = [t[0] for t in tupler]
        affix = self.make_featurelist(ordlista)
        taggar = [t[1] for t in tupler]

        #maskininlärning:
        examples = list(zip(affix,taggar))
        self.apmodel = train(5, examples)

    def make_featurelist(self, sentences):
"""
Takes sentences but returns a list with one element per word, not sentence.
Each element is a set of features for that word
"""
        flist = []
        for s in sentences:
            n = 0
            while n < len(s):
                prv = _listget(s, n-1) #returns None if none
                nxt = _listget(s, n+1) #returns None if none
                features = get_features(s[n], prevw=prv, nextw=nxt)
                flist.append(features) #adds one set per word
                n += 1
        return flist

    def predict(self, ordlista):
        #förutser taggarna som varje ord borde få utifrån den tränade LogisticRegression-estimatorn
        affixlista = self.make_featurelist(ordlista)
        tags = [self.apmodel.predict(a) for a in affixlista]
        return tags


#----------------------------------------------------------------------------------------------------
#globala funktioner
def _listget(list_,index):
    try:
        return list_[index]
    except(IndexError):
        return None

        
def read_data(fil):
    #returnerar en lista med tupler
    tupler = []    
    with open(fil, 'r') as f:
        lines = [rad for rad in f if rad != '\n'] #ignorerar blankrader
        #ord och ordklass tas fram från varje rad, vilket är 2a respektive 4e elementet:
        for line in lines:
            data = line.split()[1:4:2]
            if len(data[0]) > 3: #orden måste vara minst 3 bokstäver långa
                tupler.append((data[0],data[1])) #varje par av ord och ordklass bildar en tupel
    return tupler


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
            for i in range(1, len(word) - 1):
                if i <= max_length:
                    features.add(mark + word[-i:]) #suffix
                    if mark == '':
                        features.add(mark + word[:i] + '-p-') #prefix, only added for main word
                             
    features = set()
    _add_features(word, 5)
    _add_features(prevw, 3, '-prev-')
    _add_features(nextw, 3, '-next-')
    return features


#-------------------------------------------------------------------------------------------
#main-delen av programmet, testar algoritmen
def main(traeningsfil, testfil):
    #läser in träningsdatan och skapar TagPred.-objekt som har tränats baserat på den datan
    traeningsdata = read_data(traeningsfil)
    tagpredictor = TagPredictor(traeningsdata)

    #taggarna för testdatat förutsägs här
    testdata = read_data(testfil)
    ordlista = [tupel[0] for tupel in testdata]
    taggar = tagpredictor.predict(ordlista)
    facit_taggar = [tupel[1] for tupel in testdata]
    

    #här stäms det av hur många taggar blev korrekta och skriver ut resultaten för det
    korrekt = 0
    fel = 0
    for i in range(len(ordlista)):
        if taggar[i] == facit_taggar[i]:
            korrekt += 1
        else:
            fel += 1
    procent_korrekt = round(korrekt / len(ordlista) * 100)
    
    print("Antal korrekt taggade ord: " + str(korrekt) + "\n" +
          "Antal feltaggade ord: " + str(fel) + "\n" +
          "Andel korrekt taggade ord: " + str(procent_korrekt) + "%")

#testkörning (svenska)   
traening = os.curdir+"\sv-universal-train.conll"
test = os.curdir+"\sv-universal-test.conll"
main(traening, test)
