import streamlit as st
import pandas as pd
import os
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Load model and tokenizer
@st.cache_resource
def load_summarization_pipeline():
    model_name = "t5-small"  # You can replace this with your fine-tuned model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return pipeline("summarization", model=model, tokenizer=tokenizer)

summarizer = load_summarization_pipeline()

# Streamlit App
st.title("📝 Text Summarization App")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Single Summarization", "Batch Summarization"])

if page == "Single Summarization":
    st.header("Enter Text to Summarize")
    input_text = st.text_area("Input Text", height=300)

    max_length = st.slider("Max Summary Length", 10, 200, 60)
    min_length = st.slider("Min Summary Length", 5, 50, 10)

    if st.button("Summarize"):
        if input_text.strip():
            summary = summarizer(input_text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
            st.subheader("Summary:")
            st.success(summary)
        else:
            st.warning("Please enter some text to summarize.")

elif page == "Batch Summarization":
    st.header("Batch Summarization")
    uploaded_file = st.file_uploader("Upload CSV with a 'text' column", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if 'text' not in df.columns:
            st.error("CSV must contain a 'text' column.")
        else:
            summaries = []
            for i, txt in enumerate(df['text']):
                try:
                    summary = summarizer(txt, max_length=60, min_length=10, do_sample=False)[0]['summary_text']
                except Exception as e:
                    summary = f"Error: {str(e)}"
                summaries.append(summary)

            df['summary'] = summaries
            st.write(df)

            output_path = os.path.join("output", "summarized_batch.csv")
            os.makedirs("output", exist_ok=True)
            df.to_csv(output_path, index=False)
            st.success(f"Summarization completed. File saved to {output_path}")
