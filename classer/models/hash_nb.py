"""
Hash + Naive Bayes Model for text classification
"""

from ..embedders.hash import HashEmbedder
from ..steps.label_map import LabelMapStep
from ..classifiers.naive_bayes import NBClassifier


class HashNBModel(object):
    """Hash + Naive Bayes Model for text classification"""

    def __init__(self, data_dir):
        super(HashNBModel, self).__init__()

        self.data_dir = data_dir
        self.embedder = HashEmbedder(n_features=2 ** 10)
        self.label_mapper = LabelMapStep(data_dir=self.data_dir)
        self.classifier = NBClassifier()

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
