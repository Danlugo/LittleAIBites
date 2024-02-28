import os
import glob
import streamlit as st

directory_path = 'results'
pattern = "*.md"
files = glob.glob(os.path.join(directory_path, pattern))  # Use os.path.join for correct path construction
content = '## Contents here ##'

def show_contents(filename):
    with open(filename, "r") as file:
        content = file.read()
        return content

st.header('Results')
st.subheader('Click a file name to see the result')

for filename in files:
    if st.button(filename):
        st.markdown(show_contents(filename))