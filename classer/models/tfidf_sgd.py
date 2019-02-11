"""
TFIDF + SGD Model for text classification
"""

import json

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

from ..embedders.tfidf import TFIDFEmbedder
from ..steps.label_map import LabelMapStep
from ..classifiers.sgd import SGClassifier
from classer.utils.files import ensure_file


class TFIDFSGDModel(object):
    """TFIDF + SGD Model for text classification"""

    def __init__(self, data_dir):
        super(TFIDFSGDModel, self).__init__()

        self.data_dir = data_dir
        self.embedder = TFIDFEmbedder()
        self.label_mapper = LabelMapStep(data_dir=self.data_dir)
        self.classifier = SGClassifier()
        self.status_file = self.data_dir + 'status.json'
        ensure_file(self.status_file, {"status": "Model Initialized"})

    def get_details(self):
        """ Get a dictionary of attributes about the model to
        expose to end users for documentations purposes
        """

        return {
            "embedder": "TF-IDF",
            "algorithm": "SGD"
        }

    def get_status(self):

        return json.load(self.status_file)

    def set_status(self, status):

        with open(self.status_file, 'w') as status_file_object:
            json.dump({"status": status}, status_file_object)

    def train(self, training_data):

        samples = [example['text'] for example in training_data]
        labels = [example['label'] for example in training_data]

        self.set_status('Creating Embeddings')
        self.embedder.train(samples)
        embeddings = self.embedder.process(samples)

        self.set_status('Selecting Features')
        self.selector = SelectKBest(f_classif, k=min(20000, embeddings.shape[1]))
        self.selector.fit(embeddings, labels)
        selected_embeddings = self.selector.transform(embeddings).astype('float32')

        self.set_status('Mapping Labels')
        self.label_map = self.label_mapper.train(labels)
        label_indexes = self.label_mapper.process(labels)

        self.set_status('Training Model')
        self.classifier.train(selected_embeddings, label_indexes)
        self.set_status('Model Trained')

    def predict(self, samples):

        # TODO Pre-check that we are ready
        embeddings = self.embedder.process(samples)

        selected_embeddings = self.selector.transform(embeddings).astype('float32')
        predictions = self.classifier.process(selected_embeddings)

        classes = self.classifier.clf.classes_
        formatted = self.label_mapper.format_predictions(predictions, classes)

        return formatted
