# practical-ml-seminar
Supporting code for Practical ML for development research seminar

## Setup

```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Additionally, if you wish to make a new export from the IATI datastore API, you must create a `.env` file with an API key you can get from the IATI developer portal (https://developer.iatistandard.org/).

## To make a new export from the IATI datastore API

```
python3 datastore_api.py
```

## Notebook order

First, run `train_classifier.ipynb` either locally or on a remote python kernel.
Second, you can run `inference_classifier.ipynb` to test the model you just trained.

## Google Colab

A Google Colab implementation of this example is available [here](https://drive.google.com/file/d/1yVN2XMforQkjqFcpLtu3DCVM-nzHuxiz/view?usp=sharing).