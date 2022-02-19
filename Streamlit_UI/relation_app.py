import requests
from pyvis.network import Network
import json
import streamlit as st
import streamlit.components.v1 as components

if 'headers' not in st.session_state:
    st.session_state['headers'] = {'app-key':'12345XOXO'}

if 'blank-state' not in st.session_state:
    st.session_state['blank-state'] = True
    st.session_state['show-hide-json-state'] = False

if 'graph-html' not in st.session_state:
    st.session_state['graph-html'] = None

if 'relations-data' not in st.session_state:
    st.session_state['relations-data'] = {}

if 'color-data' not in st.session_state:
    with open('color_data.json', 'r') as f:
        color_data= json.load(f)
    st.session_state['color-data']=color_data

@st.cache
def fetch_relations(input_article):

    # with open('rel_output_new_1.json', 'r') as f:
    #     relations_data = json.load(f)
    input_json = {'article': input_article}
    relations_data= requests.post('http://localhost:1001/get_relations', json=input_json, headers = st.session_state.headers)

    return relations_data

@st.cache
def build_rel_graph_html(relations_data, physics):
    # try:
    net = Network(height="600px", width="100%", font_color="black",heading='Relations Graph', directed = True)
    
    for e in relations_data['relations_data']:
        src = e['ent1']
        dst = e['ent2']
        rel = e['relation']

        net.add_node(src['name'], src['name'], title=src['name'], color=st.session_state['color-data']['Entity'][src['tag']])
        net.add_node(dst['name'], dst['name'], title=dst['name'], color=st.session_state['color-data']['Entity'][dst['tag']])
        
        net.add_edge(source = src['name'], to = dst['name'], title=rel, color=st.session_state['color-data']['Relations'][rel])

    if physics:
        net.show_buttons(filter_=['physics'])

    net.save_graph("net_graph.html")
    return 'done'


st.markdown("""
# Simple Relation Graph Extraction
This app extract knowledge graph from an article
""")

st.header("Enter content of the article")

example_article = "Albert Einstein was a German-born theoretical physicist, widely acknowledged to be one of the greatest physicists of all time. Einstein is best known for developing the theory of relativity, but he also made important contributions to the development of the theory of quantum mechanics. Relativity and quantum mechanics are together the two pillars of modern physics. His mass–energy equivalence formula E = mc2, which arises from relativity theory, has been dubbed \"the world's most famous equation\". His work is also known for its influence on the philosophy of science. He received the 1921 Nobel Prize in Physics \"for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect\", a pivotal step in the development of quantum theory. His intellectual achievements and originality resulted in \"Einstein\" becoming synonymous with \"genius\". In 1905, a year sometimes described as his annus mirabilis ('miracle year'), Einstein published four groundbreaking papers. These outlined the theory of the photoelectric effect, explained Brownian motion, introduced special relativity, and demonstrated mass-energy equivalence. Einstein thought that the laws of classical mechanics could no longer be reconciled with those of the electromagnetic field, which led him to develop his special theory of relativity. He then extended the theory to gravitational fields; he published a paper on general relativity in 1916, introducing his theory of gravitation. In 1917, he applied the general theory of relativity to model the structure of the universe. He continued to deal with problems of statistical mechanics and quantum theory, which led to his explanations of particle theory and the motion of molecules. He also investigated the thermal properties of light and the quantum theory of radiation, which laid the foundation of the photon theory of light. However, for much of the later part of his career, he worked on two ultimately unsuccessful endeavors. First, despite his great contributions to quantum mechanics, he opposed what it evolved into, objecting that nature \"does not play dice\". Second, he attempted to devise a unified field theory by generalizing his geometric theory of gravitation to include electromagnetism. As a result, he became increasingly isolated from the mainstream of modern physics. Einstein was born in the German Empire, but moved to Switzerland in 1895, forsaking his German citizenship (as a subject of the Kingdom of Württemberg) the following year. In 1897, at the age of 17, he enrolled in the mathematics and physics teaching diploma program at the Swiss Federal polytechnic school in Zürich, graduating in 1900. In 1901, he acquired Swiss citizenship, which he kept for the rest of his life, and in 1903 he secured a permanent position at the Swiss Patent Office in Bern. In 1905, he was awarded a PhD by the University of Zurich. In 1914, Einstein moved to Berlin in order to join the Prussian Academy of Sciences and the Humboldt University of Berlin. In 1917, Einstein became director of the Kaiser Wilhelm Institute for Physics; he also became a German citizen again, this time Prussian. In 1933, while Einstein was visiting the United States, Adolf Hitler came to power in Germany. Einstein, of Jewish origin, objected to the policies of the newly elected Nazi government; he settled in the United States and became an American citizen in 1940. On the eve of World War II, he endorsed a letter to President Franklin D. Roosevelt alerting him to the potential German nuclear weapons program and recommending that the US begin similar research. Einstein supported the Allies but generally denounced the idea of nuclear weapons."
article_content = st.text_area("article content", example_article, height=250)
include_physics = st.checkbox('Include physics', value=True)

execute_button = st.button('Extract relations data')

if execute_button:
    # try:
    relations_data = fetch_relations(article_content)
    if relations_data.status_code == 200:
        if relations_data.json()['status'] == 1:
            visualize_status = build_rel_graph_html(relations_data.json(), include_physics)
            if visualize_status == 'done':
                # HtmlFile = open("net_graph.html", 'r', encoding='utf-8')
                # source_code = HtmlFile.read() 
                # with st.container():
                #     components.html(source_code, height = 1600,width=900)
                st.session_state['blank-state'] = False
                st.session_state['relations-data'] = relations_data.json()
            else:
                st.text("Error!!!, Cannot visualize the graph")
                st.session_state['blank-state'] = True
        else:
            st.text("Error!!!, Failed to extract relations data")
            st.session_state['blank-state'] = True
    else:
        st.text("Failed to extract relations!!!")
        st.session_state['blank-state'] = True
    # except:
    #     st.text("Please check relation extraction API")
    #     st.session_state['blank-state'] = True

if not st.session_state['blank-state']:

    HtmlFile = open("net_graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    with st.container():
        st.image('legend.png', width= 500 )
        components.html(source_code, height = 1150,width=900)
        show_hide_json_button = st.button('Show/Hide raw data')
    if show_hide_json_button:
        st.session_state['show-hide-json-state'] = not st.session_state['show-hide-json-state']

if st.session_state['show-hide-json-state']:
    st.json(st.session_state['relations-data'])
    object_to_download = json.dumps(st.session_state['relations-data'])    
    st.download_button(
        label="Download JSON",
        data=object_to_download,
        file_name='relations_data.json',
        mime='application/json',
    )