#!/opt/squirro/virtualenv/bin/python

'''
This is a template for a flask app
'''

import json

from flask import Flask, request, render_template, jsonify, send_from_directory

from modellab import ModelLabEnv


app = Flask(__name__)
env = ModelLabEnv()


@app.route('/env', methods=['GET'])
def get_env_details():
    """Main Route that displays the documentation"""

    env_config = env.get_env_config()
    print env_config
    return jsonify(env_config)


@app.route('/js/<path:path>', methods=['GET', 'POST'])
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>', methods=['GET', 'POST'])
def send_css(path):
    return send_from_directory('css', path)

# ----------UI----------
@app.route('/', methods=['GET'])
def fetch():
    """Main Route that displays the documentation"""

    training_list = env.list_training()
    model_list = env.list_models()
    implementation_list = env.list_implementations()
    corpus_list = env.list_corpora()
    return render_template('index.j2', trainings=training_list,
                           models=model_list,
                           implementations=implementation_list,
                           corpora=corpus_list)


@app.route('/view/training/<path:path>', methods=['GET'])
def view_training(path):
    training_name = path
    training_content = env.get_training(training_name)
    return render_template('view_training.j2', training_name=training_name,
                           training_content=training_content)


@app.route('/view/implementation/<path:path>', methods=['GET'])
def view_implementation(path):
    implementation_name = path
    implementation_config = env.get_implementation(implementation_name)
    return render_template('view_implementation.j2',
                           implementation_name=implementation_name,
                           implementation_config=implementation_config)


@app.route('/view/corpus/<path:path>', methods=['GET'])
def view_corpus(path):
    corpus_name = path
    corpus_content = env.get_corpus(corpus_name)
    return render_template('view_corpus.j2', corpus_name=corpus_name,
                           corpus_content=corpus_content)


# ----------Training----------
@app.route('/training/list', methods=['GET', 'POST'])
def list_training():

    training_list = env.list_training()
    return jsonify(training_list)


@app.route('/training/create', methods=['GET', 'POST'])
def create_training():

    training_name = request.args.get('training_name')
    training_content = request.args.get('training_data')
    env.create_training(training_name, training_content)
    return 'Success!'


@app.route('/training/get', methods=['GET', 'POST'])
def get_training():

    training_name = request.args.get('training_name')
    training_content = env.get_training(training_name)

    return jsonify(training_content)


@app.route('/training/add', methods=['GET', 'POST'])
def add_to_training():

    training_name = request.args.get('training_name')
    new_examples = request.args.get('training_data')
    try:
        new_examples = json.loads(new_examples)
    except:
        return 'The training data provided is not in a valid JSON format'

    env.add_to_training(training_name, new_examples)
    return 'Success!'


@app.route('/training/add_single', methods=['GET', 'POST'])
def add_single_to_training():

    training_name = request.args.get('training_name')
    text = request.args.get('text')
    label = request.args.get('label')

    new_examples = [{
        "text": text,
        "label": label
    }]

    env.add_to_training(training_name, new_examples)
    return 'Success!'


@app.route('/training/deduplicate', methods=['GET', 'POST'])
def deduplicate_training():

    training_name = request.args.get('training_name')
    env.deduplicate_training(training_name)

    return 'Success!'


# ----------Models----------
@app.route('/models/list', methods=['GET', 'POST'])
def list_models():

    model_list = env.list_models()
    return jsonify(model_list)


# ----------Implementations----------
@app.route('/implementations/list', methods=['GET', 'POST'])
def list_implementations():

    implementation_list = env.list_implementations()
    return jsonify(implementation_list)


# ----------Corpora----------
@app.route('/corpora/list', methods=['GET', 'POST'])
def list_corpora():

    corpus_list = env.list_corpora()
    return jsonify(corpus_list)


if __name__ == "__main__":
    app.run(port=8181, debug=True)
