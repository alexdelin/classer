"""
TFIDF Embedder Class
"""

from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFEmbedder(object):
    """TFIDF Embedder"""

    def __init__(self, stop_words='english', ngram_range=(1, 2),
                 strip_accents='unicode'):
        super(TFIDFEmbedder, self).__init__()

        self.vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                          stop_words=stop_words,
                                          ngram_range=ngram_range,
                                          strip_accents=strip_accents)

    def train(self, input_data):
        """Compute inverse document frequencies
        """

        self.vectorizer.fit(input_data)

    def process(self, input_data):
        """Split the input text into an array of tokens, and replace each
        token with the unique identifier for that token in the spacy vocab
        """

        return self.vectorizer.transform(input_data)
