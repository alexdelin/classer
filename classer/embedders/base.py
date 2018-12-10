"""
Base Embedder Class
"""

from ..steps.base import BaseStep


class BaseEmbedder(BaseStep):
    """Base Embedder class extended for implementing text embedders"""

    def __init__():
        super(BaseEmbedder, self).__init__()

    def train():
        raise NotImplementedError('This is only a base class')

    def process():
        raise NotImplementedError('This is only a base class')
