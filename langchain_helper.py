from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-pro", temperature=0.4, convert_system_message_to_human=True
)

# result = llm.invoke("does planting orange seeds give us orange tree?")

# print(result.content)

# file_path = "data/fractional_data.csv"

# loader = CSVLoader(file_path=file_path, source_column="question")

# # Store the loaded data in the 'data' variable
# data = loader.load()
# len(data)


instructor_embeddings = HuggingFaceInstructEmbeddings()

vectordb_path = "db"


def compute_and_persist_embeddings(data, embeddings, persist_dir):
    """
    Compute and persist embeddings using the Chroma class.

    Parameters:
    - data: Your input data for embedding.
    - embeddings: Your instructor embeddings.
    - persist_dir: Directory to save the embeddings.
    """

    vectordb = Chroma.from_documents(
        documents=data, embedding=embeddings, persist_directory=persist_dir
    )

    vectordb.persist()
    vectordb = None


# Call the function to compute and persist embeddings
# compute_and_persist_embeddings(data, instructor_embeddings, persist_dir)


def perform_qa(
    question, persist_dir="db", embedding_function=instructor_embeddings, llm=llm
):
    """
    Perform question-answering based on the provided question.

    Parameters:
    - question: The question for which you want an answer.
    - persist_dir: Directory where embeddings are persisted.
    - embedding_function: The embedding function (instructor_embeddings in your case).
    - llm: Language model for the retrieval chain.

    Returns:
    - answers: The answers to the given question.
    """

    # Create or load the embeddings
    vectordb = Chroma(
        persist_directory=persist_dir, embedding_function=embedding_function
    )
    retriever = vectordb.as_retriever()

    # Retrieve relevant documents
    rdocs = retriever.get_relevant_documents(question)

    # Perform question-answering using the retrieval chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
    )

    # Get answers
    answers = chain({"query": question})

    return answers


# Example usage:
# question = "What is glaucoma?"
# persist_dir = 'db'  # Your persist directory
# llm = ...  # Your language model, if available

# Call the function to perform question-answering
# result = perform_qa("tell me about Genetic Disorders")
# print(result)
