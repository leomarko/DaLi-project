import itertools
from collections import OrderedDict

#Part-of-speech pattern detection module.
#Patterns expressed in the form (LABEL--)LABEL--LABEL

class CompoundDetector:
    def __init__(self, pospatterns='standard'):
        if pospatterns == 'standard':
            pospatterns = self.standardpatterns()
        self.patterns = pospatterns

    def standardpatterns(self):
        tagset = {'AB','DT','HA','HD','HP','HS','IE','IN','JJ','KN','NN',
                  'PC','PL','PM','PN','PP','PS','RG','RO','SN','UO','VB',
                  'MAD','MID','PAD','SMS','BASE_N','IMP_V'}
        #(SUC POS-tags plus three custom tags: SMS, BASE_N and IMP_V)

        #noun-noun and noun-adjective:          
        patterns = {'BASE_N--BASE_N',
                       'BASE_N--NN',
                       'BASE_N--JJ'}

        #several combinations with imperative verb form and compounding form.
        for endtag in {'VB','IMP_V','JJ','AB','BASE_N','NN','PM'}:
            patterns.add('SMS--'+endtag)
            for prevtag in tagset - {'MAD','MID','PAD','KN','VB','IMP_V'}:
                    patterns.add(prevtag+'--IMP_V--'+endtag)
                    
        return patterns

    def detect(self, tag_sequence):
        #returns the indices of the first word of detected compounds (if any)
        compound_indices = list()
        i = 0
        while i+1 < len(tag_sequence):
            #bigram patterns
            if '--'.join(tag_sequence[i:i+2]) in self.patterns:
                compound_indices.append(i)
            #trigram patterns
            elif i > 0:
                if '--'.join(tag_sequence[i-1:i+2]) in self.patterns:
                    compound_indices.append(i)
            i += 1
            
        if len(compound_indices) == 0:
            return None
        return sorted(list(i for i in compound_indices))

    def flexibledetect(self, tagsets):
        #this function is made to use with ambiguous tagging
        compound_indices = set()
        i = 0
        while i+1 < len(tagsets):
            detection = False
            #bigram patterns
            for pattern in itertools.product(tagsets[i],tagsets[i+1]):
                if '--'.join(pattern) in self.patterns:
                    compound_indices.add(i)
                    detection = True
            #trigram patterns
            if i > 0 and not detection:
                for pattern in itertools.product(tagsets[i-1],tagsets[i],tagsets[i+1]):
                    if '--'.join(pattern) in self.patterns:
                        compound_indices.add(i)
            i += 1
            
        if len(compound_indices) == 0:
            return list() #no detections
        
        return sorted(list(i for i in compound_indices))
                
        
