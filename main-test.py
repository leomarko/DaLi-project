from postagger2 import TagPredictor
from nltk.tokenize import sent_tokenize, word_tokenize
from compounddetector import CompoundDetector
import codecs, sys, getopt

def load_postagger(path, ambiguous, min_percent):
    postagger = TagPredictor(loadpath=path,ambiguous=ambiguous, min_percent=min_percent)
    return postagger

def test_tagging(examplefile):
    with codecs.open(examplefile,'r', encoding='utf-8') as file:
        sentences = sent_tokenize(file.read(),language='swedish')
    output = [postagger.tokenize_tag(s) for s in sentences]
    for i in range(40):
        print(output[i])
        print('\n')

def detect_compounds(sentence, flexible=False):
    tags = [t[1] for t in postagger.tokenize_tag(sentence)]
    if flexible:
        return cpd.flexibledetect(tagsets)
    return cpd.detect(tags)

def compound_errors(filename, returnstring=False):
    with codecs.open(filename,'r', encoding='utf-8') as file:
        raw = file.read()
        
    sentences = sent_tokenize(raw,language='swedish')
    tagsets = list()
    for sentence in sentences:
        tagsets += [t[1] for t in postagger.tokenize_tag(sentence)]

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
                    output.append((l_index+1,w,[w for line in words for w in line][w_index+1]))
                    result=True
                    break
                w_index += 1
            l_index += 1
            
    if returnstring:
        output = ['line '+str(t[0])+': '+' '.join(t[1:3]) for t in output]
    return output    

if __name__ == '__main__':
    ambiguous = True
    min_percent = 75
    test = False
##    try:
##        opts, args = getopt.getopt(sys.argv[1:],'ht:p:')
##        for opt, arg in opts:
##            if opt == '-h':
##                print('main.py text.txt -t <testfile> -p <min_percent>')
##                sys.exit()
##            elif opt == '-t':
##                test = True
##                print(arg)
##                testfile = arg #correct answers
##            elif opt == '-p':
##                assert isinstance(arg,int) and arg > 0
##                if arg > 99:
##                    ambiguous = False
##                else:
##                    min_percent = arg
##    except getopt.GetoptError:
##        print('getopterror')
    postagger = load_postagger('apmodel_suc3iter.p', ambiguous, min_percent)
    cpd = CompoundDetector()
##    if not test:
##        with open(args[0][:-4]+'_detections.txt', 'w', encoding='utf-8') as outfile:
##            for error in compound_errors(args[0],returnstring=True):
##                outfile.write(error)
##                outfile.write('\n')
##    else:
    args = ['srsk-text.txt']
    testfile = 'srsk-facit.txt'
    with codecs.open(testfile, 'r', encoding='utf-8') as correct:
        answers = [line.split() for line in correct]
    for line in answers:
        try:
            line[0] = int(line[0])
        except(ValueError):
            line[0] = int(line[0][1:])
    answers = list(map(tuple,answers))
    detections = compound_errors(args[0])
    accurate = len([d for d in detections if d in answers])
    missed = len([a for a in answers if a not in detections])
    print('accurate: {}, missed: {}, total detections: {}'.format(accurate,missed,len(detections)))
    precision = round(accurate/len(detections), 3)
    recall = round(accurate/(accurate+missed), 3)
    f_score = round((2*precision*recall) / (precision + recall), 3)
    print('Precision: {}, Recall: {}, F-score: {}'.format(precision,recall,f_score))
