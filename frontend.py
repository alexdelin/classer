#!/opt/squirro/virtualenv/bin/python

'''
This is a template for a flask app
'''

import time
import os
import site
import sys
import urllib
import requests
import logging
import json
from logging.handlers import RotatingFileHandler

from flask import Flask, request, Response, render_template, jsonify, send_from_directory

from modellab import ModelLabEnv

app = Flask(__name__)
env = ModelLabEnv()

@app.route('/', methods=['GET'])
def fetch():
    """Main Route that displays the documentation"""

    return send_from_directory('html', 'index.html')


@app.route('/env', methods=['GET'])
def get_env_details():
    """Main Route that displays the documentation"""

    env_config = env.get_env_config()
    print env_config
    return jsonify(env_config)


@app.route('/training/get', methods=['GET', 'POST'])
def get_training():
	
	training_name = request.args.get('training_name')
	print 'Getting training: {}'.format(training_name)

	training_content = env.get_training(training_name)

	return jsonify(training_content)


@app.route('/training/add', methods=['GET', 'POST'])
def add_to_training():
	
	training_name = request.args.get('training_name')
	print 'Adding to training: {}'.format(training_name)

	new_examples = request.args.get('training_data')
	try:
		new_examples = json.loads(new_examples)
	except:
		return 'The training data provided is not in a valid JSON format'

	env.add_to_training(training_name, new_examples)

	return 'Success!'

if __name__ == "__main__":
    app.run(port=8181, debug=True)
