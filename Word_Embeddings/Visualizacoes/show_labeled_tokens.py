import os

import streamlit as st
import pandas as pd
import ast

def main():
    st.title('Data Labelling')
    UPLOADED_DATA_FOLDER = 'uploaded_data'
    LABELING_FOLDER = 'labeled_data'
    # let the user select from a list of csv files from 'uploaded_data' folder
    if os.path.exists(UPLOADED_DATA_FOLDER):
        csv_files = os.listdir(UPLOADED_DATA_FOLDER)
        csv_path = st.selectbox('Select a csv file', csv_files)
    else:
        st.warning('No txt files uploaded until now')

    df = pd.read_csv(os.path.join(UPLOADED_DATA_FOLDER, csv_path))
    df = df.iloc[:100]
    st.write(df)

    paragraph = df.iloc[0]

    def do_coloring(paragraph):

        add_colour = lambda word, label: f'<span style="color: red">{word}</span>' if label == 'LABEL_1' else f'<span style="color: green">{word}</span>'
        add_grey = lambda word, label: f'<span style="color: grey">{word}</span>'
        metaphors = [x for x in paragraph if x != 'nan' and x != '' and type(x) == str and ast.literal_eval(x)['score'] > .95 and ast.literal_eval(x)['entity'] == 'LABEL_1']

        words = [add_colour(
            ast.literal_eval(x)['word'].replace('Ġ', ' '),
            ast.literal_eval(x)['entity']
        ) if ast.literal_eval(x)['score'] > .95 else add_grey(
            ast.literal_eval(x)['word'].replace('Ġ', ' '),
            ast.literal_eval(x)['entity']) for x in paragraph if x != 'nan' and x != '' and type(x) == str]


        def check_next_word(i:int , paragraph:list)->bool:
            # this function checks if the next word is with label 1
            if i+1 < len(paragraph):
                if paragraph[i+1] == 'nan' or paragraph[i+1] == '' or type(paragraph[i+1]) != str:
                    return False

                next_word = ast.literal_eval(paragraph[i+1])
                if next_word['word'][0] == 'Ġ':
                    return False
                if next_word['entity'] == 'LABEL_1':
                    return True
            return False


        def check_previous_word(i:int , paragraph:list)->bool:
            # this function checks if the previous word is with label 1
            if i-1 >= 0:
                previous_word = ast.literal_eval(paragraph[i-1])
                if previous_word['entity'] == 'LABEL_1':
                    return True
            return False

        # words = []
        # for i, x in enumerate(paragraph):
        #     if x != 'nan' and x != '' and type(x) == str:
        #         x = ast.literal_eval(x)
        #         word = x['word'].replace('Ġ', ' ')
        #         label = x['entity']
        #         if check_next_word(i, paragraph):
        #             words.append(add_colour(word, 'LABEL_1'))
        #         else:
        #             words.append(add_colour(word, label))
        return words, metaphors

    words, metaphors = do_coloring(paragraph)

    st.markdown(''.join(words), unsafe_allow_html=True)

    # transform the words into a dataframe
    words_df = pd.DataFrame(metaphors, columns=['metaphors'])
    words_df['Correct'] = False
    words_df['Correct'] = words_df['Correct'].astype(bool)

    # let the user select the correct or incorrect words
    st.data_editor(words_df)
    # save the dataframe with the correct words
    # logging info will be the name of the file, the name of the user and the date and the words that are correct and incorrect
    logging_info = {
        'filename': csv_path,
        'user': st.session_state.username,
        'date': pd.Timestamp.utcnow(),
        'correct_words': words_df[words_df['Correct'] == True]['metaphors'].tolist(),
        'incorrect_words': words_df[words_df['Correct'] == False]['metaphors'].tolist()
    }
    # save the logging info to a csv file
    path_to_save = os.path.join(LABELING_FOLDER, csv_path)
    os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
    pd.DataFrame.from_dict(logging_info, orient='index').to_csv(path_to_save, index=False, mode='a')