import os
import json


class ModelLabEnv(object):
	"""docstring for ModelLabEnv"""


	def __init__(self, config_file='~/.model-lab.json'):

		self.env_config = self.get_env_config(config_file)
		self.data_dir = self.get_data_dir()

	
	def get_env_config(self, config_location='~/.model-lab.json'):
	
		if '~' in config_location:
			config_location = os.path.expanduser(config_location)

		with open(config_location, 'r') as env_config_file:
			env_config = json.load(env_config_file)
	
		return env_config


	def get_data_dir(self):

		return self.env_config.get('data-dir')


	def get_training(self, training_name):
		
		relative_training_path = 'training/{name}/{name}_training.json'.format(name=training_name)
		full_training_path = self.get_data_dir() + relative_training_path

		with open(full_training_path, 'r') as training_file:
			training_data = json.load(training_file)

		return training_data