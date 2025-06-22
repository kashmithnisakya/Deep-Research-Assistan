import streamlit as st
from workflows.research_graph import ResearchGraph
from config.settings import Settings
from tools.document_retriever import DocumentRetriever
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    st.set_page_config(page_title="Deep Research Assistant", layout="wide")
    st.title("Deep Research Assistant")
    st.markdown("Ask analytical questions and get detailed, reasoned answers.")

    # Initialize components
    settings = Settings()
    document_retriever = DocumentRetriever(settings)
    research_graph = ResearchGraph(settings)

    # Sidebar for document upload
    with st.sidebar:
        st.header("Upload Documents")
        st.markdown("Upload PDF or text files to enhance the document database (optional).")
        with st.form(key="upload_form"):
            uploaded_files = st.file_uploader(
                "Choose files",
                type=["pdf", "txt"],
                accept_multiple_files=True,
                help="Upload files to add to the document retrieval database."
            )
            upload_button = st.form_submit_button("Upload")

        if upload_button and uploaded_files:
            with st.spinner("Indexing documents..."):
                try:
                    logger.info(f"Uploading {len(uploaded_files)} documents.")
                    document_retriever.add_documents(uploaded_files)
                    st.success(f"Successfully indexed {len(uploaded_files)} documents!")
                except Exception as e:
                    st.error(f"Failed to index documents: {str(e)}")

    # Main form for query input
    with st.form(key="research_form"):
        query = st.text_area("Enter your question:", height=100)
        logger.info(f"User query: {query}")
        submit_button = st.form_submit_button("Get Answer")

    if submit_button and query:
        with st.spinner("Researching..."):
            try:
                result = research_graph.run(query)
                st.subheader("Answer")
                st.markdown(result["answer"])
                st.subheader("Sources")
                for source in result.get("sources", []):
                    st.write(f"- {source}")
                logger.info(f"Research completed successfully for query: {query}")
            except Exception as e:
                logger.error(f"Error during research: {str(e)}")
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()