from postagger import TagPredictor
from nltk.tokenize import sent_tokenize, word_tokenize
from compounddetector import CompoundDetector
from optparse import OptionParser
import codecs

def load_postagger(path, ambiguous, min_percent):
    postagger = TagPredictor(loadpath=path,ambiguous=ambiguous, min_percent=min_percent)
    return postagger

#single sentences
def detect_compounds(sentence, flexible=False):
    #returns the indices for the first words of detected compounds
    tags = [t[1] for t in postagger.tokenize_tag(sentence)]
    if flexible:
        return cpd.flexibledetect(tagsets)
    return cpd.detect(tags)

#whole texts
def compound_errors(filename, returnstring=False):
    #returns a list of line numbers and detected compounds,
    #either as tuples with 3 elements or as a string (if returnstring=True)
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

#-------------------------------------------Run
if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options] textfile')
    parser.add_option('-f', '--filename', dest='outfile',
                      help='specify filename for output file')
    parser.add_option('-p', '--minpercent', dest='percent', type=int, default=75,
                      help='set minimum percent of max score for POS-tags ("unambiguity level")')
    parser.add_option('-t', '--test', dest='test',
                      help='evaluate detections with testfile')
    parser.add_option('--apmodel',dest='apmodel', default='apmodel_suc3iter.p',
                      help='specify pickled averaged perceptron model to use')
    opts, args = parser.parse_args()
    ambiguous = True
    if opts.percent > 99:
        ambiguous = False

    postagger = load_postagger(opts.apmodel, ambiguous, opts.percent)
    cpd = CompoundDetector()
    
    if not opts.test:
        path = opts.outfile
        if path and path[:-4] != '.txt':
            path += '.txt'
        if not path:
            path = args[0][:-4]+'_detections.txt'  
        with open(path, 'w', encoding='utf-8') as outfile:
            for error in compound_errors(args[0],returnstring=True):
                outfile.write(error)
                outfile.write('\n')
                
    else:
        with open(opts.test, 'r', encoding='utf-8') as correct:
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
