import os
import sys
import json
import pickle


class ModelLabEnv(object):
    """docstring for ModelLabEnv"""

    def __init__(self, config_file='~/.model-lab.json'):

        self.env_config = self.get_env_config(config_file)
        self.data_dir = self.get_data_dir()
        self.cache = {
            "models": {},
            "implementations": {}
        }

    # ----------Environment----------
    def get_env_config(self, config_location='~/.model-lab.json'):

        if '~' in config_location:
            config_location = os.path.expanduser(config_location)

        with open(config_location, 'r') as env_config_file:
            env_config = json.load(env_config_file)

        return env_config

    def get_data_dir(self):

        data_dir = self.env_config.get('data-dir')
        if data_dir[-1] != '/':
            data_dir += '/'

        return data_dir

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
                print 'Skipping example with missing text or label'
                continue

            if unzipped_training.get(example.get('text')):
                if unzipped_training.get(example.get('text')) == example.get('label'):
                    continue
                else:
                    del unzipped_training[example.get('text')]
            else:
                unzipped_training[example.get('text')] = example.get('label')

        new_training = []
        for training_text, training_label in unzipped_training.iteritems():
            new_training.append({
                "text": training_text,
                "label": training_label
            })


        self.write_training(training_name, new_training)

    def recommend_training(self, corpus_name, implementation_name, amount='10'):

        try:
            amount = int(amount)
        except:
            raise ValueError('invalid amount specified')

        corpus = self.get_corpus(corpus_name)
        if len(corpus) > amount:
            corpus = corpus[:amount]

        loaded_implementations = self.list_loaded_implementations()
        if implementation_name not in loaded_implementations:
            self.load_implementation(implementation_name)

        recommendation = []
        for test_document in corpus:
            expected_label = self.evaluate_implementation(implementation_name,
                                                          test_document)
            recommendation.append({
                "text": test_document,
                "label": expected_label
            })

        return recommendation

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

        loaded_model = self.load_model_class(full_model_dir)

        self.cache.setdefault('models', {})
        self.cache['models'][model_name] = loaded_model

    def load_model_class(self, full_model_dir):

        sys.path.append(full_model_dir)
        from model import Model
        loaded_model = Model()
        sys.path.remove(full_model_dir)
        return loaded_model

    def unload_model(self, model_name):

        if self.cache['models'].get(model_name):
            del self.cache['models'][model_name]
        else:
            raise ValueError('Selected model is currently not loaded')

    def train_model(self, model_name, training_set):

        if not self.cache['models'].get(model_name):
            raise ValueError('Selected Model is currently not loaded')

        self.cache['models'][model_name].train(training_set)

    def evaluate_model(self, model_name, text):

        if not self.cache['models'].get(model_name):
            raise ValueError('Selected Model is currently not loaded')

        label = self.cache['models'][model_name].evaluate(text)
        return label

# ----------Implementations----------
    def list_implementations(self):

        implementation_dir = self.data_dir + 'implementations'
        return os.listdir(implementation_dir)

    def list_loaded_implementations(self):
        loaded_implementations = self.cache['implementations'].keys()
        print loaded_implementations
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

        # Load Selected Model
        relative_model_path = 'models/{name}/model.py'.format(name=model_name)
        full_model_path = self.data_dir + relative_model_path
        full_model_dir = os.path.dirname(full_model_path)

        loaded_model = self.load_model_class(full_model_dir)

        self.cache.setdefault('implementations', {})
        self.cache['implementations'][implementation_name] = loaded_model

        # Train with Selected Data
        training_content = self.get_training(training_name)
        self.cache['implementations'][implementation_name].train(training_content)

        # Save Trained Implementation
        self.save_implementation(implementation_name)

        # Write Implementation Config
        relative_implementation_config_path = 'implementations/{name}/'\
                                              'implementation.json'.format(
                                                    name=implementation_name)
        implementation_config_path = self.data_dir + relative_implementation_config_path

        implementation_config = {
            "model_name": model_name,
            "training_name": training_name
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

        relative_implementation_path = 'implementations/{name}/'\
                                       'implementation.pickle'.format(
                                            name=implementation_name)
        full_implementation_path = self.data_dir + relative_implementation_path

        implementation_object = self.cache['implementations'][implementation_name]

        if os.path.exists(full_implementation_path):
            raise ValueError('Implementation to create already exists')

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

        label = self.cache['implementations'][implementation_name].evaluate(text)
        return label

# ----------Corpora----------
    def list_corpora(self):
        corpora_dir = self.data_dir + 'corpora'
        return os.listdir(corpora_dir)

    def get_corpus(self, corpus_name):

        relative_corpus_path = 'corpora/{name}/corpus.json'.format(
                                    name=corpus_name)
        full_corpus_path = self.data_dir + relative_corpus_path

        with open(full_corpus_path, 'r') as corpus_file:
            corpus_data = json.load(corpus_file)

        return corpus_data
