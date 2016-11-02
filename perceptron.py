#Simple Perceptron

from collections import defaultdict
import pickle
import random

class AveragedPerceptron:
    def __init__(self, loadpath=None):
        if loadpath: #if already trained, gets the weights, which is all that's needed to predict
            self.load(loadpath)
        else:
            # Each feature is assigned a dict of weight values for each class
            # weights is a dict of those dicts
            self.weights = defaultdict(lambda: defaultdict(int))
            self.classes = set()
            # The accumulated values, for the averaging. These will be keyed by
            # feature/clas tuples
            self._totals = defaultdict(lambda: defaultdict(int))
            # The last time the feature was changed, for the averaging. Also
            # keyed by feature/clas tuples
            # (tstamps is short for timestamps)
            self._tstamps = defaultdict(lambda: defaultdict(int))
            # Number of updates
            self.updates = 0

    def get_scores(self,features):
        #returns a dictionary of the scores for classes for a collection of features
        scores = defaultdict(float)
        for feature in features:
            if feature not in self.weights:
                continue
            weights = self.weights[feature] #a dictionary of classes: values associated with the feature
            for label, weight in weights.items():
                scores[label] += weight
        return scores

    def predict(self, features):
        '''Returns the best label.'''
        scores = self.get_scores(features)
        # the set of classes is sorted by the score and secondarily the label and the label is returned
        for class_, score in scores.items():
            if score == max(scores.values()):
                return class_

    def predict_alternatives(self, features, d=False, min_percent=75):
        '''Returns the best label and the top labels if they are good enough.
           d argument toggles whether to output the score for labels or just the labels.
           Function only used for output, not training.'''
        scores = self.get_scores(features)
        labels = {label: score for label, score in scores.items() if score > max(scores.values())*min_percent*0.01}
        if d: 
            return labels
        return set(labels.keys())

    def update(self, truth, guess, features):
        '''Update the feature weights.'''
        def upd_values(clas, feat, value):
            #the total weight is sum of the weights at each update point,
            #since each feature is not updated each time, total weight is multiplied
            #by time since last update
            self._totals[feat][clas] += self.weights[feat][clas] * (self.updates - self._tstamps[feat][clas]) 
            self._tstamps[feat][clas] = self.updates
            self.weights[feat][clas] += value
            
        self.updates += 1
        if truth == guess:
            return None
        for f in features:
            #penalize incorrect predictions and add value to the correct answer
            upd_values(guess, f, -1.0)
            upd_values(truth, f, 1.0)
        return None

    def average_weights(self):
        '''Average weights from all iterations.'''
        for feat, weights in self.weights.items():
            for clas, weight in weights.items():
                self._totals[feat][clas] += weight * (self.updates - self._tstamps[feat][clas])
                averaged = round(self._totals[feat][clas] / float(self.updates), 3)
                self.weights[feat][clas] = averaged
        return None

    def save(self, path):
        '''Save the pickled model weights.'''
        return pickle.dump(dict(self.weights), open(path, 'wb'))

    def load(self, path):
        '''Load the pickled model weights.'''
        self.weights = pickle.load(open(path, 'rb'))
        return None


def train(nr_iter, examples, savedir=None):
    '''Return an averaged perceptron model trained on ``examples`` for
    ``nr_iter`` iterations.
    '''
    model = AveragedPerceptron()
    for i in range(nr_iter):
        random.shuffle(examples)
        for features, class_ in examples:
            guess = model.predict(features)
            if guess != class_:
                model.update(class_, guess, features)
    model.average_weights()
    if savedir:
        model.save(savedir)
    return model
