from postagger2 import TagPredictor
from nltk.tokenize import sent_tokenize, word_tokenize
from compounddetector import CompoundDetector
import codecs
import sys

def load_postagger(path):
    postagger = TagPredictor(loadpath=path)
    return postagger

def test_tagging(examplefile):
    with codecs.open(examplefile,'r', encoding='utf-8') as file:
        sentences = sent_tokenize(file.read(),language='swedish')
    output = [postagger.tokenize_tag(s) for s in sentences]
    for i in range(40):
        print(output[i])
        print('\n')

def detect_compounds(sentence):
    tags = [t[1] for t in postagger.tokenize_tag(sentence)]
    print(cpd.detect(tags))

def flex_detect_compounds(sentence):
    tagsets = [t[1] for t in postagger.tokenize_tag(sentence, ambiguous=True)]
    print(cpd.flexibledetect(tagsets))

def compound_errors(filename):
    with codecs.open(filename,'r', encoding='utf-8') as file:
        raw = file.read()
        
    sentences = sent_tokenize(raw,language='swedish')
    tagsets = list()
    for sentence in sentences:
        tagsets += [t[1] for t in postagger.tokenize_tag(sentence, ambiguous=True)]

    words = list()
    for line in raw.split('\n'):
        words.append(word_tokenize(line,language='swedish'))

    del raw
    assert len([w for line in words for w in line]) == len(tagsets)

    output = list()
    for detection in cpd.flexibledetect(tagsets):
        l_index = 0
        w_index = 0
        result = False
        for line in words:
            if result:
                break
            for w in line:
                if w_index == detection:
                    output.append('line '+str(l_index+1)+': '+
                                  ' '.join([w for line in words for w in line][w_index:w_index+2]))
                    result=True
                    break
                w_index += 1
            l_index += 1

    return output    

if __name__ == '__main__':
    postagger = load_postagger('apmodel_suc3iter.p')
    cpd = CompoundDetector()
    with open(sys.argv[1][:-4]+'_detections.txt', 'w', encoding='utf-8') as outfile:
        for error in compound_errors(sys.argv[1]):
            outfile.write(error)
            outfile.write('\n')


    
    #example = 'testexempel.txt'
##    example = 'wikiartikel.txt'
##    detect_compounds('Jag köpte en grävling madrass')
##    flex_detect_compounds('Jag köpte en grävling madrass')
##    detect_compounds('Jag köpte en jätte madrass')
##    flex_detect_compounds('Jag köpte en jätte madrass')
##    ans = input('Testa '+example+' ? (y/n)')
##    if ans == 'y':
##        #test_tagging(example)
##        print(compound_errors(example))
    
        
            
