import pickle
import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
# batch_size = 4
encoder_max_len = 100
tokenizer_checkpoint = "distilbert-base-uncased" 
model_dir = os.path.join(dir_path,'model')

with open(f'{model_dir}/id2label_pkl', 'rb') as f1:
    id2label = pickle.load(f1)

tokenizer = DistilBertTokenizerFast.from_pretrained(tokenizer_checkpoint, do_lower_case=True, max_length = 512)

def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

# get device
device = get_default_device()

best_model_checkpoint = f"{model_dir}/best_model_rel/"
best_model = DistilBertForSequenceClassification.from_pretrained(best_model_checkpoint)
best_model = best_model.to(device)

def predict_relasi(text):

    with torch.no_grad():
        encoder_inputs = tokenizer(text, is_split_into_words=False, truncation=True, max_length=encoder_max_len, padding='max_length', 
                                   return_overflowing_tokens=False, return_offsets_mapping=True, return_tensors="pt")   
        input_ids, attention_mask = encoder_inputs["input_ids"], encoder_inputs["attention_mask"]
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        output = best_model(input_ids = input_ids, attention_mask = attention_mask)
        logits = output.logits
        logits_labels = torch.argmax(logits, dim=1).tolist()
        label = id2label[logits_labels[0]]

    return label