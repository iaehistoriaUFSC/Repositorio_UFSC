import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import Extracao_de_dados.via_upload as vu
import Word_Embeddings.Visualizacoes.show_labeled_tokens as slt
import dashboard_visualizations as dv

# Set page config
st.set_page_config(page_title='AI in History', page_icon='📜', layout='wide', initial_sidebar_state='auto')

# Load configuration file
with open('secrets/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create an authentication object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Add login widget
name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", [
        "File Uploader",
        "Show Labeled Tokens",
        "Text Embeddings and Visualization",
    ])

    if page == "File Uploader":
        vu.get_file()
    elif page == "Show Labeled Tokens":
        slt.main()
    elif page == "Text Embeddings and Visualization":
        dv.main()

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
