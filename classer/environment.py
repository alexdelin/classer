"""
Classer - Text Classification as a service
"""

import os
import sys
import json
import pickle
import random

from classer.models import MODEL_MANIFEST
from classer.models.hash_nb import HashNBModel
from classer.models.count_sgd import CountSGDModel
from classer.models.tfidf_sgd import TFIDFSGDModel
from classer.models.tfidf_svm import TFIDFSVMModel
from classer.models.tfidf_mlp import TFIDFMLPModel
from classer.models.glove_rnn import GloveRNNModel
from classer.utils.score import score_model
from classer.utils.status import get_status
from classer.utils.files import ensure_dir, ensure_file


class ClasserEnv(object):
    """docstring for ClasserEnv"""

    def __init__(self, config_file='~/.classer.json'):

        self.env_config = self.get_env_config(config_file)
        self.data_dir = self.get_data_dir()
        self.ensure_data_dir_contents()
        self.status_file = self.data_dir + 'status.json'
        self.cache = {
            "models": {},
            "implementations": {}
        }

# ----------Environment----------
    def get_env_config(self, config_location='~/.classer.json'):

        if '~' in config_location:
            config_location = os.path.expanduser(config_location)

        with open(config_location, 'r') as env_config_file:
            env_config = json.load(env_config_file)

        return env_config

    def get_data_dir(self):

        data_dir = self.env_config.get('data-dir')

        if '~' in data_dir:
            data_dir = os.path.expanduser(data_dir)

        if data_dir[-1] != '/':
            data_dir += '/'

        return data_dir

    def get_current_status(self):

        return get_status(self.status_file)

    def ensure_data_dir_contents(self):

        # Ensure that the data dir exists
        ensure_dir(self.data_dir)
        print(self.data_dir + 'training')

        # Ensure that all sub-dirs exist
        ensure_dir(self.data_dir + 'training')
        ensure_dir(self.data_dir + 'implementations')
        ensure_dir(self.data_dir + 'corpora')

# ----------Training----------
    def list_training(self):

        training_dir = self.data_dir + 'training'
        return os.listdir(training_dir)

    def create_training(self, training_name, training_data=None):

        if not training_data:
            training_data = []

        relative_training_path = 'training/{name}/{name}_training.json'.format(
                                    name=training_name)
        full_training_path = self.data_dir + relative_training_path

        if os.path.exists(full_training_path):
            raise ValueError('Training to create already exists')

        if not os.path.exists(os.path.dirname(full_training_path)):
            os.makedirs(os.path.dirname(full_training_path))

        with open(full_training_path, 'w') as training_file:
            json.dump(training_data, training_file)

    def get_training(self, training_name):

        relative_training_path = 'training/{name}/{name}_training.json'.format(
                                    name=training_name)
        full_training_path = self.data_dir + relative_training_path

        with open(full_training_path, 'r') as training_file:
            training_data = json.load(training_file)

        return training_data

    def write_training(self, training_name, training_data):

        relative_training_path = 'training/{name}/{name}_training.json'.format(
                                    name=training_name)
        full_training_path = self.data_dir + relative_training_path

        with open(full_training_path, 'w') as training_file:
            json.dump(training_data, training_file)

    def add_to_training(self, training_name, new_examples):

        training = self.get_training(training_name)

        for new_example in new_examples:
            training.append(new_example)

        self.write_training(training_name, training)

    def deduplicate_training(self, training_name):

        training_contents = self.get_training(training_name)

        unzipped_training = {}
        for example in training_contents:

            if not example.get('text') or not example.get('label'):
                print('Skipping example with missing text or label')
                continue

            if unzipped_training.get(example.get('text')):
                if unzipped_training.get(example.get('text')) == example.get('label'):
                    continue
                else:
                    del unzipped_training[example.get('text')]
            else:
                unzipped_training[example.get('text')] = example.get('label')

        new_training = []
        for training_text, training_label in unzipped_training.items():
            new_training.append({
                "text": training_text,
                "label": training_label
            })

        self.write_training(training_name, new_training)

    def recommend_training(self, corpus_name, implementation_name,
                           amount='10', confidence=None):
        try:
            amount = int(amount)
        except:
            raise ValueError('invalid amount specified')

        if not confidence:
            confidence = 0
        else:
            confidence = float(confidence) / 100

        corpus = self.get_corpus(corpus_name)
        random.shuffle(corpus)

        loaded_implementations = self.list_loaded_implementations()
        if implementation_name not in loaded_implementations:
            self.load_implementation(implementation_name)

        recommendation = []
        for test_document in corpus:
            expected_label, label_prob = self.evaluate_implementation(
                                                implementation_name,
                                                test_document)
            if label_prob >= confidence:
                recommendation.append({
                    "text": test_document,
                    "label": expected_label,
                    "confidence": label_prob
                })

            if len(recommendation) >= amount:
                break

        return recommendation

# ----------Models----------
    def list_models(self):
        '''List all available model types which can be used to create
        implementations
        '''

        return MODEL_MANIFEST

    def benchmark_model(self, model_name, training_name):

        if self.cache.get('benchmark'):
            raise ValueError('A benchmark job is already running!')

        temp_data_dir = '{base}temp/'.format(base=self.data_dir)

        # make the temp folder if it doesn't exist already
        if not os.path.exists(temp_data_dir):
            os.makedirs(temp_data_dir)

        if model_name == 'hash_nb':
            loaded_model = HashNBModel(data_dir=temp_data_dir)

        elif model_name == 'count_sgd':
            loaded_model = CountSGDModel(data_dir=temp_data_dir)

        elif model_name == 'tfidf_sgd':
            loaded_model = TFIDFSGDModel(data_dir=temp_data_dir)

        elif model_name == 'tfidf_svm':
            loaded_model = TFIDFSVMModel(data_dir=temp_data_dir)

        elif model_name == 'tfidf_mlp':
            loaded_model = TFIDFMLPModel(data_dir=temp_data_dir)

        elif model_name == 'glove_rnn':
            loaded_model = GloveRNNModel(data_dir=temp_data_dir)

        else:
            raise ValueError('Unknown model type ' + model_name)

        self.cache['benchmark'] = loaded_model
        dataset = self.get_training(training_name)

        benchmark = score_model(self.cache['benchmark'], dataset, self.status_file)
        del self.cache['benchmark']
        return benchmark

    def get_benchmark_progress(self):
        '''Get progress for an in-progress benchmarking task
        if applicable. This only works because you can run one
        benchmarking task at a time
        '''

        if not self.cache.get('benchmark'):
            raise ValueError('No benchmark task currently running')
        else:
            return self.cache['benchmark'].get_status()

# ----------Implementations----------
    def list_implementations(self):

        implementation_dir = self.data_dir + 'implementations'
        return os.listdir(implementation_dir)

    def list_loaded_implementations(self):
        loaded_implementations = self.cache['implementations'].keys()
        return loaded_implementations

    def get_implementation(self, implementation_name):

        relative_implementation_path = 'implementations/{name}/'\
                                       'implementation.json'.format(
                                            name=implementation_name)
        full_implementation_path = self.data_dir + relative_implementation_path

        with open(full_implementation_path, 'r') as implementation_file:
            implementation_data = json.load(implementation_file)

        return implementation_data

    def create_implementation(self, model_name, training_name,
                              implementation_name):

        # Early Exit
        if self.cache.get('implementations', {}).get(implementation_name):
            raise ValueError('Implementation already exists!')

        implementation_data_dir = '{base}implementations/{name}/'.format(
                                        base=self.data_dir,
                                        name=implementation_name)

        # make the implementation folder if it doesn't exist already
        if not os.path.exists(implementation_data_dir):
            os.makedirs(implementation_data_dir)

        if model_name == 'hash_nb':
            loaded_model = HashNBModel(data_dir=implementation_data_dir)

        elif model_name == 'tfidf_sgd':
            loaded_model = TFIDFSGDModel(data_dir=implementation_data_dir)

        elif model_name == 'tfidf_svm':
            loaded_model = TFIDFSVMModel(data_dir=implementation_data_dir)

        else:
            raise ValueError('Unknown model type ' + model_name)

        self.cache.setdefault('implementations', {})
        self.cache['implementations'][implementation_name] = loaded_model

        # Train with Selected Data
        training_content = self.get_training(training_name)
        self.cache['implementations'][implementation_name].train(training_content)

        # Save Trained Implementation
        self.save_implementation(implementation_name)

        # Write Implementation Config
        implementation_config_path = '{base}implementations/{name}/'\
                                     'implementation.json'.format(
                                        base=self.data_dir,
                                        name=implementation_name)

        implementation_config = {
            "model_name": model_name,
            "training_name": training_name,
            "number_examples": len(training_content)
        }

        with open(implementation_config_path, 'w') as implementation_config_file:
            json.dump(implementation_config, implementation_config_file)

    def load_implementation(self, implementation_name):

        # Early Exit
        if self.cache.get('implementations', {}).get(implementation_name):
            raise ValueError('Implementation is already loaded!')

        relative_implementation_path = 'implementations/{name}/'\
                                       'implementation.pickle'.format(
                                            name=implementation_name)
        full_implementation_path = self.data_dir + relative_implementation_path

        # Add model dir to path before loading
        implementation_config_path = os.path.join(
            os.path.dirname(full_implementation_path),
            'implementation.json')
        with open(implementation_config_path, 'r') as implementation_config_file:
            implementation_config = json.load(implementation_config_file)

        model_name = implementation_config.get('model_name')
        relative_model_path = 'models/{name}/model.py'.format(name=model_name)
        full_model_path = self.data_dir + relative_model_path
        full_model_dir = os.path.dirname(full_model_path)
        sys.path.append(full_model_dir)

        with open(full_implementation_path, 'r') as implementation_file:
            loaded_implementation = pickle.load(implementation_file)

        sys.path.remove(full_model_dir)

        self.cache['implementations'][implementation_name] = loaded_implementation

    def save_implementation(self, implementation_name):

        # TODO - Implement this in the library, and just call the .save() method

        relative_implementation_path = 'implementations/{name}/'\
                                       'implementation.pickle'.format(
                                            name=implementation_name)
        full_implementation_path = self.data_dir + relative_implementation_path

        implementation_object = self.cache['implementations'][implementation_name]

        #if os.path.exists(full_implementation_path):
        #    raise ValueError('Implementation to create already exists')

        if not os.path.exists(os.path.dirname(full_implementation_path)):
            os.makedirs(os.path.dirname(full_implementation_path))

        with open(full_implementation_path, 'w') as implementation_file:
            pickle.dump(implementation_object, implementation_file)

    def unload_implementation(self, implementation_name):

        if self.cache['implementations'].get(implementation_name):
            del self.cache['implementations'][implementation_name]
        else:
            raise ValueError('Selected implementation is currently not loaded')

    def evaluate_implementation(self, implementation_name, text):

        if not self.cache['implementations'].get(implementation_name):
            raise ValueError('Selected Implementation is currently not loaded')

        prediction = self.cache['implementations'][implementation_name].predict(text)
        return prediction

    def reimplement(self, implementation_name):

        implementation_config = self.get_implementation(implementation_name)
        model_name = implementation_config.get('model_name')
        training_name = implementation_config.get('training_name')

        # Unload current implementation from memory
        if implementation_name in self.list_loaded_implementations():
            self.unload_implementation(implementation_name)

        # Re-build Implementation
        self.create_implementation(model_name, training_name, implementation_name)

# ----------Corpora----------
    def list_corpora(self):
        corpora_dir = self.data_dir + 'corpora'
        return os.listdir(corpora_dir)

    def get_corpus(self, corpus_name, amount=None):

        relative_corpus_path = 'corpora/{name}/corpus.json'.format(
                                    name=corpus_name)
        full_corpus_path = self.data_dir + relative_corpus_path

        with open(full_corpus_path, 'r') as corpus_file:
            corpus_data = json.load(corpus_file)

        if amount:
            selection = random.sample(corpus_data, amount)
            return selection

        return corpus_data
