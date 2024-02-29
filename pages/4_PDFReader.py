import streamlit as st
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from common.PDFBot import PDFBot
import socket

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

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

if "question_disabled" not in st.session_state:
    st.session_state.question_disabled = True

# Side Bar configuration
with st.sidebar:
    # for locall development, create .streamlit folder with secreats.toml file
    image_path = st.secrets.logo
    st.image(image_path, width=100)
    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")

    # if running from my local machine
    hostname = socket.gethostname()
    if 'Daniels-iMac.local' in hostname:
        openai_key = st.secrets.openai['key']
        openai_api_key = openai_key
    
    b = PDFBot(openai_api_key)

    if openai_api_key:
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
    else:
        st.write('Please add the Openai api key to enable program.')


question = st.chat_input("Ask questions about your documents:", disabled=st.session_state.question_disabled)

if question:
    if openai_key:
            openai_api_key = openai_key

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    handle_userinput(question)
