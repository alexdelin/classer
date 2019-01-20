"""
Support Vector Classifier Class
"""

from sklearn.svm import SVC


class SVMClassifier(object):
    """Support Vector Classifier"""

    def __init__(self):
        super(SVMClassifier, self).__init__()

        # Enable prediction with probabilities
        self.clf = SVC(probability=True)

    def train(self, training_data, labels):

        self.clf.fit(training_data, labels)

    def process(self, process_data):

        # TODO Add the label map and return probabilities for
        # the original class names
        return self.clf.predict_proba(process_data)
