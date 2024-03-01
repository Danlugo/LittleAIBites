import streamlit as st
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from common.PDFBot import PDFBot
import socket

# Configuration
image_path = 'images/side_bar_bot_01.png'
st.set_page_config(page_title="PDFReader", page_icon=None, layout="wide", initial_sidebar_state="expanded")

if not 'side_bar_image' in st.session_state:
    st.session_state.side_bar_image = image_path

if not 'openai_api_key' in st.session_state:
    st.session_state['openai_api_key'] = None

if not 'disable_functionality' in st.session_state:
    st.session_state['disable_functionality'] = True

if not 'question_disabled' in st.session_state:
    st.session_state['question_disabled'] = True

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(':smile:       ' + message.content)
            #st.write(user_template.replace(
            #    "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(':robot_face:       ' + message.content)
            #st.write(bot_template.replace(
            #    "{{MSG}}", message.content), unsafe_allow_html=True)


st.title("🔎 Chat with multiple PDFS :books:")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM, OpenAI Embeddings, Vector (FAISS) DB and PyPDF2")

st.write(css, unsafe_allow_html=True)


# Side Bar configuration
with st.sidebar:
    # for locall development, create .streamlit folder with secreats.toml file
    st.image(image_path, width=100)

    if 'openai_api_key' in st.session_state:
        #st.write(st.session_state.openai_api_key)
        if not st.session_state.openai_api_key == None:
            if not st.session_state.openai_api_key == '':
                st.info("OpenAI enabled")
        else:
            st.warning("Please add your OpenAI API key on the main page to continue.")

    if 'disable_functionality' in st.session_state:
        st.write('Disabled', st.session_state.disable_functionality)
        pass

    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    
    if not 'openai_api_key' in st.session_state:
        st.info("Please add your OpenAI API key on the main page to continue.")
        st.stop()
    else:

        try:
            b = PDFBot(st.session_state.openai_api_key)

            if pdf_docs:
                if st.button("Process"):
                    with st.spinner("Processing"):
                        # get pdf text
                        raw_text = b.get_pdf_text(pdf_docs)

                        # get the text chunks
                        text_chunks = b.get_text_chunks(raw_text)

                        # create vector store
                        vectorstore = b.get_vectorstore(text_chunks)

                        # create conversation chain
                        st.session_state.conversation = b.get_conversation_chain(vectorstore)

                        # enable
                        st.session_state.question_disabled = False

                        # Tell user that he/she is ready to ask questions
                        st.info('Documents Processed!!, Please use the prompt to ask questions')
        except Exception as e:
            st.warning('There was an error. Please make sure API Key is valid')
            pass

# MAIN BODY
question = st.chat_input("Ask questions about your documents:", disabled=st.session_state.question_disabled)

if question:
    handle_userinput(question)
