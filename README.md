# Classer

Tools for Testing and benchmarking text classification models

## Installation

Install Classer by running:
```bash
$ pip install -r requirements.txt
$ python setup.py develop
```

## Setup

Before running classer, create your config file at `~/.classer.json`. You can create this by copying the sample version in `cofig/example_config.json` then editing the file as needed. 

```bash
$ cp config/example_config.json ~/.classer.json
```

This file stores the basic parameters about how classer operates, such as where it stores its data.

## Usage

To run classer, move into the frontend folder and run the script `api.py`. This will start a flask app that runs on port `8181`. You can then access the web UI for classer from a browser.

```bash
$ cd frontend
$ python api.py
 * Serving Flask app "api" (lazy loading)
...
 * Running on http://0.0.0.0:8181/ (Press CTRL+C to quit)
```

With classer running, you can go to the address `http://localhost:8181` in a browser to set up and use classer
