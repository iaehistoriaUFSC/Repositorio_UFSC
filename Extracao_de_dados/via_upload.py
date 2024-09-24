import pandas as pd
from transformers import pipeline
import streamlit as st
import os
from itertools import chain

FOLDER_PATH = 'uploaded_data/'

def get_file():
    st.title('File uploader')

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # check if file is a txt file
        if uploaded_file.name.split('.')[-1] != 'txt':
            st.write('Please upload a txt file')
            return
        book = uploaded_file.read().decode('utf-8').split('\n')
        st.write(book)
        st.write('File uploaded')
        st.write('Running the model...')
        pipe = pipeline("token-classification", model="CreativeLang/metaphor_detection_roberta_seq")

        book = [l for l in book if l != '\n']
        paragraphs = [l for l in book if len(l) > 100]
        # Use the pipeline to detect metaphors in a sentence
        # Use the pipeline to detect metaphors in a sentence
        sentences = {}
        for i, p in enumerate(paragraphs):
            sentences[p] = []
            for s in p.split('.'):
                if len(s) > 0:
                    sentences[p].append(pipe(s))
                    print(f'{i} - {s}')


        st.write('Model finished running')

        df_paragraphs = pd.DataFrame(list(chain(*[w for w in sentences.values()])))

        file_name = uploaded_file.name.split('.')[0]

        st.write('Saving the results...')

        os.makedirs(FOLDER_PATH, exist_ok=True)
        path_to_save = os.path.join(FOLDER_PATH, f'{file_name}.csv')
        df_paragraphs.to_csv(path_to_save, index=False)
        st.write('Results saved')
        st.write(df_paragraphs)
