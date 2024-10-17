import streamlit as st
import sentencepiece as spm
import pandas as pd

# Load amharic sentencepiece tokenizer
sp = spm.SentencePieceProcessor()
sp.load('model/amharic_toknizer_v2.model')

st.title("Amharic Text Tokenizer")

# Input area for Amharic text
with st.form("tokenization_form"):
    amharic_text = st.text_area("Enter Amharic Text:", height=150)
    tokenize_button = st.form_submit_button("Tokenize")

if tokenize_button:
    if not amharic_text:
        st.warning("Please enter Amharic text.")
    else:
        try:
            # Tokenize the text
            encoded_text = sp.encode_as_pieces(amharic_text)
            encoded_vector = sp.encode_as_ids(amharic_text)

            # Display the tokenized output
            st.subheader("Tokenized Output:")
            st.write("Tokens:")
            st.code(encoded_text)
            st.write("Token IDs:")
            st.code(encoded_vector)

            # Add a download button for the tokenized output
            @st.cache_data
            def convert_to_csv(encoded_text, encoded_vector):
                df = pd.DataFrame({"Token": encoded_text, "ID": encoded_vector})
                return df.to_csv(index=False)

            csv = convert_to_csv(encoded_text, encoded_vector)
            st.download_button("Download Tokenized Output", csv, "tokenized_output.csv", "text/csv")

        except Exception as e:
            st.error(f"Error during tokenization: {e}")
