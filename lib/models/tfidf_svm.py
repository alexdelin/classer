"""
TFIDF + SGD Model for text classification
"""

from ..embedders.tfidf import TFIDFEmbedder
from ..steps.label_map import LabelMapStep
from ..classifiers.svm import SVMClassifier


class TFIDFSVMModel(object):
    """TFIDF + SGD Model for text classification"""

    def __init__(self, data_dir):
        super(TFIDFSVMModel, self).__init__()

        self.data_dir = data_dir
        self.embedder = TFIDFEmbedder()
        self.label_mapper = LabelMapStep(data_dir=self.data_dir)
        self.classifier = SVMClassifier()

    def train(self, training_data):

        samples = [example['text'] for example in training_data]
        labels = [example['label'] for example in training_data]

        self.embedder.train(samples)
        embeddings = self.embedder.process(samples)

        self.label_map = self.label_mapper.train(labels)
        label_indexes = self.label_mapper.process(labels)

        self.classifier.train(embeddings, label_indexes)

    def predict(self, samples):

        # TODO Pre-check that we are ready
        embeddings = self.embedder.process(samples)

        predictions = self.classifier.process(embeddings)

        classes = self.classifier.clf.classes_
        formatted = self.label_mapper.format_predictions(predictions, classes)

        return formatted
