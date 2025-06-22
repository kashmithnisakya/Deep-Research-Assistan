import streamlit as st
from workflows.research_graph import ResearchGraph
from config.settings import Settings

def main():
    st.set_page_config(page_title="Deep Research Assistant", layout="wide")
    st.title("Deep Research Assistant")
    st.markdown("Ask analytical questions and get detailed, reasoned answers.")

    settings = Settings()
    research_graph = ResearchGraph(settings)

    with st.form(key="research_form"):
        query = st.text_area("Enter your question:", height=100)
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
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()