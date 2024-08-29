import streamlit as st
import pandas as pd
import numpy as np
from pdf2image import  convert_from_bytes
from io import BytesIO
from PIL import Image
import random

# Load the PDF
pdf_path = "Overview_of_Client_Projects_V3.pdf"  # Update with your PDF file path

# Extract pages as images
def extract_pdf_pages(pdf_path):
    pages = convert_from_bytes(open(pdf_path, 'rb').read())
    return pages

# Display pages
pages = extract_pdf_pages(pdf_path)

# Define the options based on the number of pages
num_options = len(pages)
options = [f"Option {i+1}" for i in range(num_options)]

# Create a DataFrame for storing pairwise comparison results
matrix = pd.DataFrame(0, index=options, columns=options)

# Streamlit UI
st.title("Find your ideal Statistical Consulting topic")
st.write("Author : Vinson")

# Sample 50% of the pairs
def generate_pairs(options, sample_fraction=0.5):
    pairs = [(options[i], options[j]) for i in range(len(options)) for j in range(i + 1, len(options))]
    return random.sample(pairs, int(len(pairs) * sample_fraction))

# Initialize session state
if 'pairs' not in st.session_state:
    st.session_state.pairs = generate_pairs(options)
    st.session_state.current_index = 0
    st.session_state.matrix = pd.DataFrame(0, index=options, columns=options)
    st.session_state.current_choice = None  # Store the current choice

# Show the current comparison
def show_comparison(pair):
    option1, option2 = pair
    col1, col2 = st.columns(2)

    with col1:
        st.image(pages[options.index(option1)], caption=option1, use_column_width=True)
    
    with col2:
        st.image(pages[options.index(option2)], caption=option2, use_column_width=True)


# Show the comparison if there are still pairs to show
if st.session_state.current_index < len(st.session_state.pairs):
    current_pair = st.session_state.pairs[st.session_state.current_index]
    option1, option2 = current_pair
    show_comparison(current_pair)
    
    with st.form("my_form"):
        choice = st.radio(f"Which is better?", [option1, option2], key=f"{option1}_{option2}")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
        
            if choice == option1:
                st.session_state.matrix.loc[option1, option2] += 1
            else:
                st.session_state.matrix.loc[option2, option1] += 1
            
            # Move to the next comparison
        st.session_state.current_index += 1
else:
    st.write("All comparisons are done!")

# Button to calculate the results
if st.button("Calculate Rankings") or st.session_state.current_index == len(st.session_state.pairs):
    # Calculate the total scores
    scores = st.session_state.matrix.sum(axis=1)
    
    # Rank the options
    ranking = scores.sort_values(ascending=False)
    
    # Display results
    st.write("Ranking of options:")
    st.write(ranking)

    # Show pairwise comparison matrix
    st.write("Pairwise Comparison Matrix:")
    st.write(st.session_state.matrix)
