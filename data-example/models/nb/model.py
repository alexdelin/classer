from textblob.classifiers import NaiveBayesClassifier


class Model(object):
    """docstring for Model"""
    def __init__(self, name='Guess', config={}):
        self.name = name
        self.config = config
        self.clf = NaiveBayesClassifier([])

    def train(self, training_data):

        safe_training = []

        for example in training_data:
            safe_training.append((example.get('text'), example.get('label')))

        self.clf.update(safe_training)

    def evaluate(self, text):
        label = self.clf.classify(text)
        prob_dist = self.clf.prob_classify(text)
        label_prob = prob_dist.prob(label)
        return label, label_prob

    def get_classes(self):
        return self.clf.labels()

    def save(self):
        pass

    def load(self):
        pass
