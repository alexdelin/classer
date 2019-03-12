#!/usr/bin/env/python
'''
Upload Sample Training Data
'''

import json

import requests

API_BASE_URL = 'http://localhost:8181'

TRAININGS = {
    'Movie Sentiment': 'movie_sentiment_training.json',
    '20 Newsgroups Easy': '20_newsgroups_easy_training.json',
    '20 Newsgroups Hard': '20_newsgroups_hard_training.json'
}


for training_name, training_path in TRAININGS.iteritems():

    print('Loading Training {name}'.format(name=training_name))

    # Check that the training doesn't already exist
    previous_trainings = json.loads(
        requests.get(API_BASE_URL + '/training/list').text)

    if training_name in previous_trainings:
        raise ValueError('Training {name} already exists!'.format(
                            name=training_name))

    # Load the training from disk
    with open(training_path, 'r') as training_file_object:
        training_data = json.load(training_file_object)

    # Create the training
    response = requests.post(
                    API_BASE_URL + '/training/create',
                    params={'training_name': training_name},
                    data=json.dumps(training_data))
    if response.status_code > 299:
        raise ValueError('Got Invalid Response {} from server'.format(
                            response.status_code))
