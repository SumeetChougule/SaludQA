import streamlit as st
from langchain_helper import compute_and_persist_embeddings, perform_qa

st.title("Salud QA")
btn = st.button("Create Knowledgebase")

if btn:
    pass


question = st.text_input("Question: ")

if question:
    response = perform_qa(question)

    st.header("Answer: ")
    st.write(response["result"])
