import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import dashboard_visualizations as dv
import Word_Embeddings.Visualizacoes.show_labeled_tokens as slt
import Extracao_de_dados.via_upload as vu

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
        "Text Embeddings and Visualization",
        "Show Labeled Tokens",
        "File Uploader"

    ])

    if page == "Text Embeddings and Visualization":
        dv.main()
    elif page == "Show Labeled Tokens":
        slt.main()
    elif page == "File Uploader":
        vu.get_file()
        
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


