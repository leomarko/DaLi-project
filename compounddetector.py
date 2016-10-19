class CompoundDetector:
    def __init__(self, pospatterns='standard'):
        if pospatterns == 'standard':
            pospatterns = self.standardpatterns()
        self.patterns = pospatterns

    def standardpatterns(self):
        tagset = {'AB','DT','HA','HD','HP','HS','IE','IN','JJ','KN','NN',
                  'PC','PL','PM','PN','PP','PS','RG','RO','SN','UO','VB',
                  'MAD','MID','PAD','SMS','BASE_N','IMP_V'}
                  
        patterns = {'BASE_N--BASE_N',
                       'BASE_N--NN',
                       'BASE_N--JJ'}

        for endtag in {'VB','IMP_V','JJ','AB','BASE_N','NN','PM'}:
            patterns.add('SMS--'+endtag)
            for prevtag in tagset - {'MAD','MID','PAD','KN','VB','IMP_V'}:
                if prevtag not in {'MAD','MID','PAD','KN','VB','IMP_V'}:
                    patterns.add(prevtag+'--IMP_V--'+endtag)
                    
        return patterns
    
    def load_tagger(self, tagpredictor):
        self.tgp = tagpredictor

    def detect(self, tag_sequence):
        compound_indices = list()
        i = 0
        while i < len(tag_sequence):
            try:
                if tag_sequence[i] + '--' + tag_sequence[i+1] in self.patterns:
                    compound_indices.append(i)
                i += 1
            except(IndexError):
                break
        if len(compound_indices) == 0:
            return None
        return compound_indices
            
                
        
