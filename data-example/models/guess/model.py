import random


class Model(object):
	"""docstring for Model"""
	def __init__(self, name='Guess', config={}):
		super(Model, self).__init__()
		self.name = name
		self.config = config

	def train(self, training_data):
		pass

	def evaluate(self, text):
		return random.choice(self.get_classes())

	def get_classes(self):
		return ['pos', 'neg']

	def save(self):
		pass

	def load(self):
		pass
