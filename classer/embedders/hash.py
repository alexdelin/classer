"""
Hash Embedder Class
"""

from sklearn.feature_extraction.text import HashingVectorizer


class HashEmbedder(object):
    """TFIDF Embedder"""

    def __init__(self, n_features=2**18):
        super(HashEmbedder, self).__init__()

        self.vectorizer = HashingVectorizer(stop_words='english',
                                            decode_error='ignore',
                                            n_features=n_features,
                                            alternate_sign=False)

    def train(self, input_data):
        """Nothing to do
        """

        pass

    def process(self, input_data):
        """Transform the input text into an array of tokens with
        counts of each
        """

        return self.vectorizer.transform(input_data)
