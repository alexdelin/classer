"""
Naive Bayes Classifier Class
"""

from sklearn.naive_bayes import BernoulliNB


class NBClassifier(object):
    """Naive Bayes Classifier"""

    def __init__(self):
        super(NBClassifier, self).__init__()

        # Enable prediction with probabilities
        self.clf = BernoulliNB()

    def train(self, training_data, labels):

        self.clf.fit(training_data, labels)

    def process(self, process_data):

        # TODO Add the label map and return probabilities for
        # the original class names
        return self.clf.predict_proba(process_data)
