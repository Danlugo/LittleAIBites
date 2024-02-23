import os
import json
import socket
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import streamlit as st
import webbrowser
import streamlit as st
from streamlit.components.v1 import html

class GoogleAuth:
    """
    created by dgonzalez on 2024-02-22 - initial structure to separate authentication from streamlit webcode
    """
    _version = 0.1

    def __init__(self) -> None:
        self.image_path = st.secrets.logo
        self.fqdn = socket.getfqdn()
        self.hostname = socket.gethostname()
        self.current_path = os.getcwd()
        self.client_id = st.secrets.google_auth['client_id']
        self.client_secret = st.secrets.google_auth['client_secret_key']
        self.secret_file = st.secrets.google_auth['secret_file_path']
        self.client_config = json.loads(st.secrets['config'])
        self.redirect_uri = "https://littleaibites-smyg87hdmugauhmn5t9yjq.streamlit.app/"

        if os.path.isfile(self.secret_file):
            print('Found File', self.secret_file)
            with open (self.secret_file, 'r') as f:
                f.readline()
                print(f.readline())
        else:
            print('Didnt find File', self.secret_file)

        if 'codespaces' in self.hostname:
            self.redirect_uri = "https://obscure-sniffle-x5x67wq5663vqrp-8501.app.github.dev/"

        print('OS PATH',self.current_path)


    def open_page(url):
        open_script= """<script type="text/javascript">window.open('%s', '_blank').focus();</script>""" % (url)
        html(open_script)

    def auth_flow(self):
        auth_code = st.query_params.get("code")


        if os.path.isfile(self.secret_file):
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                self.secret_file,
                scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
                redirect_uri=self.redirect_uri,
            )
        else:

            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config=self.client_config,
                scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
                redirect_uri=self.redirect_uri
            )

        if auth_code:
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            user_info_service = build(
                serviceName="oauth2",
                version="v2",
                credentials=credentials,
            )
            user_info = user_info_service.userinfo().get().execute()
            assert user_info.get("email"), "Email not found in infos"
            st.session_state["google_auth_code"] = auth_code
            st.session_state["user_info"] = user_info
            
        else:
            st.image(self.image_path, width=300)
            if st.button("Sign in with Google"):
                authorization_url, state = flow.authorization_url(access_type="offline",include_granted_scopes="true",)
                self.open_page(authorization_url)
                #webbrowser.open_new_tab(authorization_url)


# https://discuss.streamlit.io/t/how-to-link-a-button-to-a-webpage/1661/7