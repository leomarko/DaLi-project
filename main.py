from postagger2 import TagPredictor
from nltk.tokenize import sent_tokenize
import codecs

def load_postagger(path):
    postagger = TagPredictor(loadpath=path)
    return postagger

def test_tagging(examplefile):
    with codecs.open(examplefile,'r', encoding='utf-8') as file:
        sentences = sent_tokenize(file.read(),language='swedish')
    output = [postagger.tokenize_tag(s) for s in sentences]
    for line in output:
        print(line)
        print('\n')

if __name__ == '__main__':
    postagger = load_postagger('apmodel_suc3iter.p')    
    #example = 'testexempel.txt'
    example = 'wikiartikel.txt'
    ans = input('Testa '+example+' ? (y/n)')
    if ans == 'y':
        test_tagging(example)
        
            
