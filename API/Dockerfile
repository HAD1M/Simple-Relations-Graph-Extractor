FROM python:3.7

RUN pip install spacy==2.1.0
RUN pip install neuralcoref
RUN python -m spacy download en
RUN pip install torch==1.7.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install transformers==4.2.2
RUN pip install numpy==1.19.5
RUN pip install nltk==3.5
RUN python -m nltk.downloader 'punkt'
RUN pip install fastapi
RUN pip install "uvicorn[standard]"

copy NER NER/
copy Relation_Classification Relation_Classification/
copy /relations_graph_extractor.py /
copy /api.py /

CMD [ "python","-u","-W ignore", "./api.py" ]