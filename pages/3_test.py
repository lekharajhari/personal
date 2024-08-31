import streamlit as st
import time

# Function to multiply the input number with numbers from 1 to 20
def multiply_number(input_number):
    results_placeholder = st.empty()  # Placeholder for results

    results = []
    for i in range(1, 21):
        result = input_number * i
        results.append(f"{input_number} x {i} = {result}")
        
        # Update the page with all results so far using st.success
        with results_placeholder.container():
            for res in results:
                st.success(res)
        
        time.sleep(1)  # Simulate processing time

    # Final message after the loop completes
    st.write("Multiplication completed!")

# Streamlit app
st.title("Multiplication Status Tracker")

# Input from the user
input_number = st.number_input("Enter a number", min_value=1, max_value=1000, value=1)

# Button to start the multiplication
if st.button("Start Multiplication"):
    multiply_number(input_number)