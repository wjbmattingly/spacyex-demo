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

st.title("spaCyEx Demo")

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