import numpy as np
import torch
from transformers import DistilBertForTokenClassification, DistilBertTokenizerFast
import pickle
import nltk
import os

# nltk.download('punkt')
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

file_path = os.path.dirname(os.path.realpath(__file__))
idtagdir = os.path.join(file_path, 'idtag')

with open(f'{idtagdir}/tag2id_pkl', 'rb') as f1:
    tag2id = pickle.load(f1)

with open(f'{idtagdir}/id2tag_pkl', 'rb') as f2:
    id2tag = pickle.load(f2)

encoder_max_len = 300

tokenizer_checkpoint = "distilbert-base-uncased" 
tokenizer = DistilBertTokenizerFast.from_pretrained(tokenizer_checkpoint, do_lower_case=True, max_length=512)

model_checkpoint = os.path.join(file_path, "model/checkpoint-10530/")
model = DistilBertForTokenClassification.from_pretrained(model_checkpoint)

# set get device function
def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

device = get_default_device()       
model = model.to(device)

def model_predict(text):

  word_token = nltk.word_tokenize(text)
  tokenized_input_text = tokenizer(word_token, is_split_into_words=True, return_offsets_mapping=True, max_length=encoder_max_len, padding='max_length', truncation=True, 
                                   return_tensors="pt")
  input_ids, attention_mask, offset_mapping = tokenized_input_text["input_ids"], tokenized_input_text["attention_mask"], tokenized_input_text["offset_mapping"]
  input_ids = input_ids.to(device)
  attention_mask = attention_mask.to(device)
  output = model(input_ids = input_ids, attention_mask = attention_mask)
  logits = output.logits
  logits_labels = torch.argmax(logits, dim=-1).tolist()
  tag = np.array([id2tag[i] for i in logits_labels[0]])
  # since by the tokenizer some word are splitted, so we need to map the output label using the offset_mapping into the right token
  arr_offset = offset_mapping.numpy()[0]
  mask = (arr_offset[:,0] == 0) & (arr_offset[:,1] != 0)
  return word_token, tag[mask].tolist()

def main_process(input_):

    try:
        word_token, tag = model_predict(input_)
        output = list(zip(word_token, tag))
        status = 1

    except Exception as e:
        status = 0
        output = []
        print(e)

    return {"status": status, "tagged": output}