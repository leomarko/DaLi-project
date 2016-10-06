import re

class CompableDict:
    def __init__(self,featurelist):
        self.prefixscores = dict()
        self.suffixscores = dict()

        #remove duplicate word entries
        featurelist = [string for string in featurelist if not re.match(r'-(prev|next)-',string)]

        words = [string[:-3] for string in featurelist if re.search(r'-w-$',string)]
        words = [w for w in words if words.count(w) > 5]
        prefixes = [string[:-3] for string in featurelist if re.search(r'-p-$',string)]
        suffixes = [string[:-3] for string in featurelist if re.search(r'-s-$',string)]

        for word in words:
            p = prefixes.count(word)
            s = suffixes.count(word)
            if p > 1:
                self.prefixscores[word] = p
            if s > 1:
                self.suffixscores[word] = s

    def show(self):
        print('prefixscores')
        print(self.prefixscores)
        print('suffixscores')
        print(self.suffixscores)

def word_to_tag_dict(scores, apmodel):
    tagscores = dict()
    for word in scores.keys():
        tag = apmodel.predict(word)
        if tag in tagscores:
            tagscores[tag] += scores[word]
        else:
            tagscores[tag] = scores[word]
    return tagscores
            
        
    
