"""
Stochastic Gradient Descent Classifier Class
"""

from sklearn.linear_model import SGDClassifier

from ..steps.base import BaseStep


class SGClassifier(object):
    """Stochastic Gradient Descent Classifier"""

    def __init__(self):
        super(SGClassifier, self).__init__()

        # Use log loss function to enable incremental
        # training and prediction with probabilities
        self.clf = SGDClassifier(loss="log")

    def train(self, training_data, labels):

        self.clf.fit(training_data, labels)

    def process(self, process_data):

        # TODO Add the label map and return probabilities for
        # the original class names
        return self.clf.predict_proba(process_data)
