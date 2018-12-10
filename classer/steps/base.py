"""
Base Step Class
"""


class BaseStep(object):
    """Base Step class extended for implementing all other steps"""

    def __init__(self, data_dir):
        super(BaseStep, self).__init__()

        self.data_dir = data_dir

    def train():
        raise NotImplementedError('This is only a base class')

    def process():
        raise NotImplementedError('This is only a base class')
