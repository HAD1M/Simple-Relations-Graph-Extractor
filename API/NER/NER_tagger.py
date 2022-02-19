import re
import copy
from .NER_predictor import main_process as tag_main_process

def clean_text(Kalimat):
    
    Kalimat = re.sub("  ", " ", Kalimat)
    Kalimat = re.sub("\( ", "(", Kalimat)
    Kalimat = re.sub(" \)", ")", Kalimat)
    Kalimat = Kalimat.strip()
    return Kalimat

def pred_tag_loc(Kalimat):
    
    result = tag_main_process(clean_text(Kalimat))
    return result

def get_tag_coordinates(tag_output_test):
    
    tag_coor_set=[]
    tag_coor = []
    ent_label = []
    sign_tag = ['B-LOC', 'B-ORG', 'B-PER', 'I-LOC', 'I-ORG', 'I-PER']
    for i in range(len(tag_output_test)):
        if tag_output_test[i][1] in sign_tag:
            if not ent_label:
                ent_label.append(tag_output_test[i][1])
                tag_coor.append(i)
            else:
                if tag_output_test[i][1][2:] == ent_label[0][2:]:
                    pass
                else:
                    tag_coor.append(i) 
                    tag_coor_set.append({"coor":tag_coor, "tag": ent_label[0][2:]})
                    ent_label=[]
                    tag_coor = []
                    ent_label.append(tag_output_test[i][1])
                    tag_coor.append(i)


        else:
            if ent_label:
                tag_coor.append(i)
                tag_coor_set.append({"coor":tag_coor, "tag": ent_label[0][2:]})
                ent_label=[]
                tag_coor = []
            else:
                pass
    
    return tag_coor_set


def get_tokens_kalimat(tag_output):
    
    tokens_kalimat = []
    for word_label in tag_output:
        tokens_kalimat.append(word_label[0])

    return tokens_kalimat

def get_input_kalimat_tagged(kalimat_raw, tag_coor1, tag_coor2, tags_add = ('<e1>', '</e1>', '<e2>', '</e2>')):

    tags_coor = tag_coor1['coor'] + tag_coor2['coor']
    kalimat_out = copy.copy(kalimat_raw)
    for i in range(4):
        kalimat_out.insert(tags_coor[i]+i, tags_add[i])

    return ' '.join(kalimat_out)

