#!/opt/squirro/virtualenv/bin/python

'''
This is a template for a flask app
'''

import json

from flask import Flask, request, render_template, jsonify, send_from_directory

from modellab import ModelLabEnv


app = Flask(__name__)
env = ModelLabEnv()


@app.route('/', methods=['GET'])
def fetch():
    """Main Route that displays the documentation"""

    training_list = env.list_training()
    return render_template('index.j2', trainings=training_list)


@app.route('/view/training/<path:path>', methods=['GET'])
def view_training(path):
    """Main Route that displays the documentation"""

    training_content = env.get_training(path)
    return render_template('view_training.j2', training_name=path,
                           training_content=training_content)


@app.route('/env', methods=['GET'])
def get_env_details():
    """Main Route that displays the documentation"""

    env_config = env.get_env_config()
    print env_config
    return jsonify(env_config)


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


@app.route('/models/list', methods=['GET', 'POST'])
def list_models():

    model_list = env.list_models()
    return jsonify(model_list)


if __name__ == "__main__":
    app.run(port=8181, debug=True)
