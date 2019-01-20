"""
Count + SGD Model for text classification
"""

from ..embedders.count import CountEmbedder
from ..steps.label_map import LabelMapStep
from ..classifiers.sgd import SGClassifier


class CountSGDModel(object):
    """Count + SGD Model for text classification"""

    def __init__(self, data_dir):
        super(CountSGDModel, self).__init__()

        self.data_dir = data_dir
        self.embedder = CountEmbedder()
        self.label_mapper = LabelMapStep(data_dir=self.data_dir)
        self.classifier = SGClassifier()

    def get_details(self):
        """ Get a dictionary of attributes about the model to
        expose to end users for documentations purposes
        """

        return {
            "embedder": "Count",
            "algorithm": "SGD"
        }

    def save(self, save_dir):
        pass

    def load(self, save_dir):
        pass

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
