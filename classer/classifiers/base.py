"""
Base Classifier Class
"""

from ..steps.base import BaseStep


class BaseClassifier(BaseStep):
    """Base Classifier class extended for implementing text classifiers"""

    def __init__(self):
        super(BaseClassifier, self).__init__()

    def train(self, training_data):
        raise NotImplementedError('This is only a base class')

    def process(self, process_data):
        raise NotImplementedError('This is only a base class')
