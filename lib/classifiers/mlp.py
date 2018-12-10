"""
Multilayer Perceptron Classifier Class
"""

from sklearn.neural_network import MLPClassifier

from ..steps.base import BaseStep


class MLClassifier(object):
    """Multilayer Perceptron Classifier"""

    def __init__(self, hidden_layer_sizes=(64, 64), solver='adam'):
        super(MLClassifier, self).__init__()

        # Use log loss function to enable incremental
        # training and prediction with probabilities
        self.clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes,
                                 solver=solver)

    def train(self, training_data, labels):

        self.clf.fit(training_data, labels)

    def process(self, process_data):

        # TODO Add the label map and return probabilities for
        # the original class names
        return self.clf.predict_proba(process_data)
