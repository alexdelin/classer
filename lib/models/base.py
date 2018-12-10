"""
Base Model Class
"""

from ..steps.base import BaseStep


class BaseModel(BaseStep):
    """Base Model class extended for implementing text classification models"""

    def __init__(self):
        super(BaseModel, self).__init__()

    def train():
        raise NotImplementedError('This is only a base class')

    def process():
        raise NotImplementedError('This is only a base class')
