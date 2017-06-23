from nltk.tag import StanfordNERTagger

st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
st.tag('Rami Eid is studying at Stony Brook University in NY'.split())

https://spacy.io/docs/usage/entity-recognition
