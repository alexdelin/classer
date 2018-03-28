import os
import sys
import json


class ModelLabEnv(object):
	"""docstring for ModelLabEnv"""


	def __init__(self, config_file='~/.model-lab.json'):

		self.env_config = self.get_env_config(config_file)
		self.data_dir = self.get_data_dir()
		self.cache = {}

	
	def get_env_config(self, config_location='~/.model-lab.json'):
	
		if '~' in config_location:
			config_location = os.path.expanduser(config_location)

		with open(config_location, 'r') as env_config_file:
			env_config = json.load(env_config_file)
	
		return env_config


	def get_data_dir(self):

		return self.env_config.get('data-dir')

	# ----------Training----------
	def list_training(self):

		training_dir = self.data_dir + 'training'
		return os.listdir(training_dir)


	def create_training(self, training_name, training_data=[]):
		
		relative_training_path = 'training/{name}/{name}_training.json'.format(name=training_name)
		full_training_path = self.data_dir + relative_training_path

		if os.path.exists(full_training_path):
			raise ValueError('Training to create already exists')

		os.makedirs(os.path.dirname(full_training_path))

		with open(full_training_path, 'r') as training_file:
			json.dump(training_data, training_file)


	def get_training(self, training_name):
		
		relative_training_path = 'training/{name}/{name}_training.json'.format(name=training_name)
		full_training_path = self.data_dir + relative_training_path

		with open(full_training_path, 'r') as training_file:
			training_data = json.load(training_file)

		return training_data


	def write_training(self, training_name, training_data):
		
		relative_training_path = 'training/{name}/{name}_training.json'.format(name=training_name)
		full_training_path = self.data_dir + relative_training_path

		with open(full_training_path, 'w') as training_file:
			json.dump(training_data, training_file)


	def add_to_training(self, training_name, new_examples):
		
		training = self.get_training(training_name)

		for new_example in new_examples:
			training.append(new_example)

		self.write_training(training_name, training)


	def deduplicate_training(self, training_name):
		
		raise NotImplementedError


	# ----------Models----------
	def list_models(self):
		
		model_dir = self.data_dir + 'models'
		return os.listdir(model_dir)


	def load_model(self, model_name):
		
		# Early Exit
		if self.cache.get('models', {}).get(model_name):
			raise ValueError('Model is already loaded!')

		relative_model_path = 'models/{name}/model.py'.format(name=model_name)
		full_model_path = self.data_dir + relative_model_path
		full_model_dir = os.path.dirname(full_model_path)

		sys.path.append(full_model_dir)
		from model import Model

		self.cache.setdefault('models', {})
		self.cache['models'][model_name] = Model()

		sys.path.remove(full_model_dir)