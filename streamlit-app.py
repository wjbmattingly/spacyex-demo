import streamlit as st
import spacy
from spacy import displacy
import spacy.cli
import spacyex as se
from spacy.matcher import Matcher
from spacy.tokens import Span

@st.cache_resource
def load_model(model="en_core_web_sm"):
    try:
         nlp = spacy.load(model)
    except Exception:
        pass
    # Loading the model
    nlp = spacy.load(model)
    blank = spacy.blank("en")
    blank.add_pipe("entity_ruler")
    return nlp, blank


nlp, blank = load_model()

st.image("https://github.com/wjbmattingly/spacyex/blob/main/images/spacyex-logo.png?raw=true")

st.markdown("""
[![PyPI version](https://badge.fury.io/py/spacyex.svg)](https://pypi.org/project/spacyex/)
[![GitHub stars](https://img.shields.io/github/stars/wjbmattingly/spacyex.svg?style=social&label=Star&maxAge=2592000)](https://github.com/wjbmattingly/spacyex/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/wjbmattingly/spacyex.svg?style=social&label=Fork&maxAge=2592000)](https://github.com/wjbmattingly/spacyex/network)
""")

st.markdown("""
    <a href="https://github.com/wjbmattingly/spacyex/tree/main" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="30" height="30" style="vertical-align:bottom"/>
        Check it out on GitHub!
    </a><br><br>""", unsafe_allow_html=True)


pattern = st.text_input("Type Pattern", "(ent_type=PERSON) (lemma=in[run,walk]) (pos=in[ADV,ADJ])")
col1, col2 = st.columns(2)
text = col1.text_area("Text to Analyze", "John runs slowly. Jeff walks quickly")

if st.button("Run"):

    doc = blank(text)

    matcher_pattern = se.create_pattern(pattern)


    result = se.search(pattern, text, nlp)

    entities = []
    for r in result:
        hit, start, end = r
        span = Span(doc, start, end, label=" ")
        entities.append(span)

    doc.ents = entities

    st.json(matcher_pattern)

    ent_html = displacy.render(doc, style="ent", jupyter=False)
    # Display the entity visualization in the browser:
    col2.write("Results:")
    col2.markdown(ent_html, unsafe_allow_html=True)