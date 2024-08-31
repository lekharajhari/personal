import random
from datetime import datetime
import streamlit as st

# Function to generate a single code
def generate_code():
    """Generate a single code with 16 digits, starting with 4 or 5"""
    first_digit = str(random.choice([4, 5]))
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    return first_digit + remaining_digits

# Function to generate an expiration date
def generate_expiration_date():
    """Generate an expiration date in the format MM|YYYY"""
    current_year = datetime.now().year
    year = random.randint(current_year, 2028)
    if year==2024:
        month= random.randint(10, 12)
    else:
        month = random.randint(1, 12)
    return f"{month:02d}|{year}"

# Function to generate a random 3-digit number
def generate_random_number():
    """Generate a random 3-digit number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

# Function to generate multiple codes
def generate_multiple_codes(num):
    """Generate multiple codes with expiration dates and random numbers"""
    outputs = []
    for _ in range(num):
        code = generate_code()
        expiration_date = generate_expiration_date()
        random_number = generate_random_number()
        output = f"{code}|{expiration_date}|{random_number}"
        outputs.append(output)
    return outputs

# Function to save output to a file
def save_output_to_file(outputs):
    """Save the generated codes to a file"""
    filename = datetime.now().strftime("%Y%m%d") + ".txt"
    file_content = '\n'.join(outputs)
    return filename, file_content

# Streamlit UI
st.title("Code Generator")

# Input from the user
num_to_generate = st.number_input("Enter the number of codes to generate:", min_value=1, value=1)

# Button to generate and download the file
if st.button("Generate Codes"):
    generated_outputs = generate_multiple_codes(num_to_generate)
    filename, file_content = save_output_to_file(generated_outputs)
    
    # Provide the file for download
    st.download_button(
        label="Download Codes",
        data=file_content,
        file_name=filename,
        mime="text/plain"
    )