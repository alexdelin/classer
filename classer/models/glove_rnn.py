"""
TFIDF + SGD Model for text classification
"""


class GloveRNNModel(object):
    """Recurrent Neural Network Model for text classification"""

    def __init__(self, data_dir):
        super(GloveRNNModel, self).__init__()
        self.data_dir = data_dir

    def get_details(self):
        """ Get a dictionary of attributes about the model to
        expose to end users for documentations purposes
        """

        return {
            "embedder": "GloVe",
            "algorithm": "RNN-LSTM"
        }

    def train(self, training_data):

        raise NotImplementedError('This model is not yet implemented')

    def predict(self, samples):

        raise NotImplementedError('This model is not yet implemented')
