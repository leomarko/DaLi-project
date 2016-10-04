from postagger2 import TagPredictor
import os

def load_postagger(path):
    postagger = TagPredictor(path)
    return postagger

def test_tagging(examplefile):
    output = []
    with open(examplefile,'r') as file:
        for line in file:
            tagged = postagger.tokenize_tag(line.strip('\n'))
            output.append(tagged)
    for line in output:
        print(line)
        print('\n')

if __name__ == '__main__':
    postagger = load_postagger('apmodel.p')
    example = 'testexempel.txt'
    ans = input('Testa '+example+' ? (y/n)')
    if ans == 'y':
        test_tagging(example)
        
            
