"""
TFIDF + MLP Model for text classification
"""

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

from ..embedders.tfidf import TFIDFEmbedder
from ..steps.label_map import LabelMapStep
from ..classifiers.mlp import MLClassifier


class TFIDFMLPModel(object):
    """TFIDF + MLP Model for text classification"""

    def __init__(self, data_dir):
        super(TFIDFMLPModel, self).__init__()

        self.data_dir = data_dir
        self.embedder = TFIDFEmbedder()
        self.label_mapper = LabelMapStep(data_dir=self.data_dir)
        self.classifier = MLClassifier()

    def get_details(self):
        """ Get a dictionary of attributes about the model to
        expose to end users for documentations purposes
        """

        return {
            "embedder": "TF-IDF",
            "algorithm": "MLP"
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

        self.selector = SelectKBest(f_classif, k=min(20000, embeddings.shape[1]))
        self.selector.fit(embeddings, labels)
        selected_embeddings = self.selector.transform(embeddings).astype('float32')

        self.label_map = self.label_mapper.train(labels)
        label_indexes = self.label_mapper.process(labels)

        self.classifier.train(embeddings, label_indexes)

    def predict(self, samples):

        # TODO Pre-check that we are ready
        embeddings = self.embedder.process(samples)

        selected_embeddings = self.selector.transform(embeddings).astype('float32')
        predictions = self.classifier.process(selected_embeddings)

        classes = self.classifier.clf.classes_
        formatted = self.label_mapper.format_predictions(predictions, classes)

        return formatted
