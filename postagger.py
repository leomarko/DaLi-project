#importer
from perceptron2 import train
import os
# -*- coding: utf-8 -*-


#----------------------------------------------------------------------------------------
# klassen TagPredictor med sina funktioner nedan
class TagPredictor():
    def __init__(self, tupler):
        #datasortering, gör lista med särdrag för varje ord,
        #och lista med taggar som matchar den:
        ordlista = [t[0] for t in tupler]
        affix = self.skapa_affixlista(ordlista)
        taggar = [t[1] for t in tupler]

        #maskininlärning:
        examples = list(zip(affix,taggar))
        self.apmodel = train(5, examples)

    def skapa_affixlista(self, ordlista):
        #skapar vektorutrymme inkl. en vektor för varje affix
        #returnerar lista med uppslagslistor
        affixlista = []
        for o in ordlista:
            affix = ta_fram_affix(o)
            affixlista.append(affix) #för varje ord läggs ett set affix till
        return affixlista

    def predict(self, ordlista):
        #förutser taggarna som varje ord borde få utifrån den tränade LogisticRegression-estimatorn
        affixlista = self.skapa_affixlista(ordlista)
        tags = [self.apmodel.predict(a) for a in affixlista]
        return tags


#----------------------------------------------------------------------------------------------------
#globala funktioner
def laes_data(fil):
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


def ta_fram_affix(straeng):
    #tar fram alla affix som är högst 5 bokstäver från ett ord
    #ett ord antas ha en rot som är minst 2 bokstäver
    #markerar affixen med ett bindesträck före om det är ett suffix, och efter om det är ett prefix
    #returns a set
    affix = set()
    for i in range(1, len(straeng) - 1):
        if i < 6:
            affix.add(straeng[:i] + "-")
            affix.add("-" + straeng[-i:])
    return affix


#-------------------------------------------------------------------------------------------
#main-delen av programmet, testar algoritmen
def main(traeningsfil, testfil):
    #läser in träningsdatan och skapar TagPred.-objekt som har tränats baserat på den datan
    traeningsdata = laes_data(traeningsfil)
    tagpredictor = TagPredictor(traeningsdata)

    #taggarna för testdatat förutsägs här
    testdata = read_data("/home/corpora/universal_treebanks_v1.0/sv/sv-universal-test.conll")
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
