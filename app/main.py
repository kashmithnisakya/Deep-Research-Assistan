import streamlit as st
from workflows.research_graph import ResearchGraph
from config.settings import Settings
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

    settings = Settings()
    research_graph = ResearchGraph(settings)

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