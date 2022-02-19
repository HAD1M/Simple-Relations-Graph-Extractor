from NER import NER_tagger
from Relation_Classification import rel_classificator
from nltk.tokenize import sent_tokenize
import spacy
import neuralcoref

nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)


class_group = {
'ORG:located at(e1,e2)': ['org:stateorprovince_of_headquarters(e1,e2)', 'org:city_of_headquarters(e1,e2)', 'org:country_of_headquarters(e1,e2)'],
'ORG:located at(e2,e1)': ['org:stateorprovince_of_headquarters(e2,e1)', 'org:city_of_headquarters(e2,e1)', 'org:country_of_headquarters(e2,e1)'],
'PER:located at(e1,e2)': ['per:countries_of_residence(e1,e2)', 'per:cities_of_residence(e1,e2)', 'per:stateorprovinces_of_residence(e1,e2)'],
'PER:located at(e2,e1)': ['per:countries_of_residence(e2,e1)', 'per:cities_of_residence(e2,e1)', 'per:stateorprovinces_of_residence(e2,e1)'],
'PER:member of(e1,e2)': ['org:founded_by(e1,e2)', 'per:employee_of(e1,e2)', 'org:top_members/employees(e1,e2)'],
'PER:member of(e2,e1)': ['org:founded_by(e2,e1)', 'per:employee_of(e2,e1)', 'org:top_members/employees(e2,e1)']
}

# get relations information from a sentence
def sentence_get_all_relation(input_kalimat):
    
    tag_output = NER_tagger.pred_tag_loc(input_kalimat)['tagged']
    
    tag_coor = NER_tagger.get_tag_coordinates(tag_output)
    
    kalimat_raw = NER_tagger.get_tokens_kalimat(tag_output)

    len_all_tag = len(tag_coor)
    relations = []

    if len_all_tag>1: 

        for i in range(0, len_all_tag-1):
            tag_coor1 = tag_coor[i] 
            for j in range(i+1, len_all_tag):
                tag_coor2 = tag_coor[j]

                input_kalimat = NER_tagger.get_input_kalimat_tagged(kalimat_raw, tag_coor1, tag_coor2)

                result = rel_classificator.predict_relasi(input_kalimat)

                if result in class_group['ORG:located at(e1,e2)']:
                    if tag_coor1['tag'] == 'ORG' and tag_coor2['tag'] == 'LOC':
                        result = 'located at'
                        direction = "left"
                    else:
                        result = "Other"
                elif result in class_group['ORG:located at(e2,e1)']:
                    if tag_coor1['tag'] == 'LOC' and tag_coor2['tag'] == 'ORG':
                        result = 'located at'
                        direction = "right"
                    else:
                        result = "Other"
                elif result in class_group['PER:located at(e1,e2)']:
                    if tag_coor1['tag'] == 'PER' and tag_coor2['tag'] == 'LOC':
                        result = 'located at'
                        direction = "left"
                    else:
                        result = "Other"
                elif result in class_group['PER:located at(e2,e1)']:
                    if tag_coor1['tag'] == 'LOC' and tag_coor2['tag'] == 'PER':
                        result = 'located at'
                        direction = "right"
                    else:
                        result = "Other"
                elif result in class_group['PER:member of(e1,e2)']:
                    if tag_coor1['tag'] == 'PER' and tag_coor2['tag'] == 'ORG':
                        result = 'member of'
                        direction = "left"
                    else:
                        result = "Other"
                elif result in class_group['PER:member of(e2,e1)']:
                    if tag_coor1['tag'] == 'ORG' and tag_coor2['tag'] == 'PER':
                        result = 'member of'
                        direction = "right"
                    else:
                        result = "Other"
                elif result=='per:origin(e1,e2)':
                    if tag_coor1['tag'] == 'PER' and tag_coor2['tag'] == 'LOC':
                        result = "origin"  
                        direction = "left"
                    else:
                        result = "Other"
                elif result=='per:origin(e2,e1)':
                    if tag_coor1['tag'] == 'LOC' and tag_coor2['tag'] == 'PER':
                        result = "origin"  
                        direction = "right"
                    else:
                        result = "Other"       
                else:
                    result = 'Other'

                ent1 = ' '.join(kalimat_raw[tag_coor1['coor'][0]:tag_coor1['coor'][1]])
                ent2 = ' '.join(kalimat_raw[tag_coor2['coor'][0]:tag_coor2['coor'][1]])

                if result != 'Other':
                    if direction == "left":
                        relasi = {'ent1': {"name":ent1, 'tag':tag_coor1['tag']}, 'ent2': {"name": ent2, 'tag':tag_coor2['tag']}, 'relation': result}
                    else:
                        relasi = {'ent1': {"name": ent2, 'tag':tag_coor2['tag']}, 'ent2': {"name":ent1, 'tag':tag_coor1['tag']}, 'relation': result}

                    if not relasi in relations:
                        relations.append(relasi)            
    return relations

def article_get_relation(article):
    
    # process the article with coreference resilution by huggingface neuralcoref
    doc=nlp(article)
    coref_article = doc._.coref_resolved
    # print(coref_article)
    # parse article into sentences
    sentences = sent_tokenize(coref_article)
    
    output = []
    # for every sentece get the relations informations
    for sent in sentences:
        result = sentence_get_all_relation(sent)
        for e in result:
            # make sure there is no double elements in the  output
            if e not in output:
                output.append(e)

    return output