"""
Dictionary Embedder Class
"""

import spacy

from .base import BaseEmbedder


class DictionaryEmbedder(BaseEmbedder):
    """Base Embedder class extended for implementing text embedders"""

    def __init__(self, spacy_pkg='en_vectors_web_lg', embedding_length=None):
        super(DictionaryEmbedder, self).__init__()

        self.nlp = spacy.load(spacy_pkg)
        self.embedding_length = embedding_length

    def train(self, input_data):
        """Training is not required because spacy stores the vocab
        """
        pass

    def process(self, input_data):
        """Split the input text into an array of tokens, and replace each
        token with the unique identifier for that token in the spacy vocab
        """

        spacy_doc = self.nlp(unicode(input_data))

        embeddings = []

        for token in spacy_doc:
            embeddings.append(token.rank)

            if self.embedding_length \
                    and len(embeddings) == self.embedding_length:
                break

        if self.embedding_length and len(embeddings) < self.embedding_length:
            embeddings.extend([0] * self.embedding_length - len(embeddings))

        return embeddings
