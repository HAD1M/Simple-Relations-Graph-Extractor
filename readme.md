# Simple Relation Graph Extractor

This app extract entity objects and its relation between.

The entities consist of <span style="color:#17eee1">**PER:person**</span>, <span style="color:#17ee17">**ORG:Organization**</span> and <span style="color:#eed417">**LOC:Location**</span>.

The relations extracted are <span style="color:#f0c637">**'located at'**</span>, <span style="color:#2fe044">**'member of'**</span> and <span style="color:#c7440f">**'origin'**</span>.

## How is the system works

![image info](images/how_system_works.png)

The text article will be processed to resolve the coreference in pronouns or nouns, after that we detect the entities in every sentence and at the end we classify the relation for each sentence consisting at least two detected entities.

For coreference resolution model, I use neuralcoref from huggingface and spacy 2.1.0. ( Thanks a lot [Huggingface 🤗](https://huggingface.co/) and [Spacy](https://spacy.io/) )

For NER and Relation Classifier, I trained distilbert using conllpp and KPB7 dataset for each task respectively. 

## Here a demo of the app

![image info](images/demo.gif)

## To run the apps
### 1. Run the API

- install docker if you haven't
- cd to inside folder API/
- run `docker-compose up --build`

### 2. Run Streamlit app

- cd to inside folder Streamlit_UI
- run `streamlit run realation_app.py --server.port [PORT_NUMBER]`