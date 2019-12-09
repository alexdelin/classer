"""
Label Map Step
"""

import json

from classer.steps.base import BaseStep


class LabelMapStep(BaseStep):
    """Label Map Step"""

    def __init__(self, data_dir):
        super(BaseStep, self).__init__()

        self.data_dir = data_dir

    def train(self, labels):
        '''Create the label map from the set of training examples
        '''

        unique_labels = list(set(labels))

        label_map = {
            "forward": {},
            "backward": {}
        }

        for idx, label in enumerate(unique_labels):
            label_map['forward'][label] = idx
            label_map['backward'][idx] = label

        with open(self.data_dir + 'label_map.json', 'w') as label_map_file:
            json.dump(label_map, label_map_file)

        self.label_map = label_map

        return label_map

    def process(self, labels):
        '''Use the label map to change the labels to their indexes
        '''

        if not self.label_map:
            with open(self.data_dir + 'label_map.json', 'r') as label_map_file:
                self.label_map = json.load(label_map_file)

        return [self.label_map['forward'][label] for label in labels]

    def format_predictions(self, predictions, classes):

        formatted_predictions = []

        for prediction in predictions:

            formatted_prediction = {}

            for idx, probability in enumerate(prediction):
                class_id = classes[idx]
                class_name = self.label_map['backward'][class_id]
                formatted_prediction[class_name] = probability

            formatted_predictions.append(formatted_prediction)

        return formatted_predictions
