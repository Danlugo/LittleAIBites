import streamlit as st
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from common.PDFBot import PDFBot



def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

    
b = PDFBot()

st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

st.write(css, unsafe_allow_html=True)

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

# Side Bar configuration
with st.sidebar:
    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
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


st.header("Chat with multiple PDFs :books:")
user_question = st.chat_input("Ask a question about your documents:")

if user_question:
    handle_userinput(user_question)
