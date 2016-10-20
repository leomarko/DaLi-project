from postagger2 import TagPredictor
from nltk.tokenize import sent_tokenize
from compounddetector import CompoundDetector
import codecs

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

def output_compound_errors(file):

if __name__ == '__main__':
    postagger = load_postagger('apmodel_suc3iter.p')
    cpd = CompoundDetector()
    #example = 'testexempel.txt'
    example = 'wikiartikel.txt'
    detect_compounds('Jag köpte en grävling madrass')
    flex_detect_compounds('Jag köpte en grävling madrass')
    detect_compounds('Jag köpte en jätte madrass')
    flex_detect_compounds('Jag köpte en jätte madrass')
    ans = input('Testa '+example+' ? (y/n)')
    if ans == 'y':
        test_tagging(example)
        
            
