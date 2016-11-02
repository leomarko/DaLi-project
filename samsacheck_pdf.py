#Compound error checker using part-of-speech tagging
#and part-of-speech pattern detection
#Input in pdf-form.
#Early development version, unstable results

from postagger import TagPredictor
from nltk.tokenize import sent_tokenize, word_tokenize
from compounddetector import CompoundDetector
from optparse import OptionParser
import codecs, PyPDF2

def load_postagger(path, ambiguous, min_percent):
    postagger = TagPredictor(loadpath=path,ambiguous=ambiguous, min_percent=min_percent)
    return postagger

#whole texts
def compound_errors(filename, returnstring=False):
    #returns a list of line numbers and detected compounds,
    #either as tuples with 3 elements or as a string (if returnstring=True)
    with open(filename,'rb') as file:
        pdf = PyPDF2.PdfFileReader(file)
        number_pages = pdf.getNumPages()
        output = list()
        for p_index in range(number_pages):
            text = pdf.getPage(p_index).extractText()
            
            sentences = sent_tokenize(text,language='swedish')
            tagsets = list()
            for sentence in sentences:
                tagsets += [t[1] for t in postagger.tokenize_tag(sentence)]

            words = list()
            for line in text.split('\n'):
                words.append(word_tokenize(line,language='swedish'))

            assert len([w for line in words for w in line]) == len(tagsets)

            for detection in cpd.flexibledetect(tagsets):
                l_index = 0
                w_index = 0
                result = False
                for line in words:
                    if result:
                        break
                    for w in line:
                        if w_index == detection:
                            output.append((p_index+1, l_index+1, w, [w for line in words for w in line][w_index+1]))
                            result=True
                            break
                        w_index += 1
                    l_index += 1
                
    if returnstring:
        output = ['page '+str(t[0])+' line '+str(t[1])+': '+' '.join(t[2:4]) for t in output]
    return output    

#-------------------------------------------Run
if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options] textfile')
    parser.add_option('-f', '--filename', dest='outfile',
                      help='specify filename for output file')
    parser.add_option('-p', '--minpercent', dest='percent', type=int, default=75,
                      help='set minimum percent of max score for POS-tags ("unambiguity level")')
    parser.add_option('--apmodel',dest='apmodel', default='apmodel_newest3iter.p',
                      help='specify pickled averaged perceptron model to use')
    opts, args = parser.parse_args()
    ambiguous = True
    if opts.percent > 99:
        ambiguous = False

    postagger = load_postagger(opts.apmodel, ambiguous, opts.percent)
    cpd = CompoundDetector()
    path = opts.outfile
    if path and path[:-4] != '.txt':
        path += '.txt'
    if not path:
        path = args[0][:-4]+'_detections.txt' 
    with open(path, 'w', encoding='utf-8') as outfile:
        for error in compound_errors(args[0],returnstring=True):
            outfile.write(error)
            outfile.write('\n')
