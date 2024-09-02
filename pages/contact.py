import streamlit as st
import requests

# Updated FastAPI base URL
api_url = "https://code-api-q53u.onrender.com/contacts"

st.title("Contacts Management App")

# Create a new contact
st.header("Create a New Contact")
name = st.text_input("Name")
number = st.text_input("Number")
city = st.text_input("City")

if st.button("Create Contact"):
    if name and number:
        contact = {"name": name, "number": number, "city": city}
        response = requests.post(api_url + "/", json=contact)
        if response.status_code == 200:
            st.success("Contact created successfully!")
        else:
            st.error(f"Error: {response.json()['detail']}")
    else:
        st.error("Name and Number are required fields")

# Read a contact by name
st.header("Find a Contact by Name")
find_name = st.text_input("Enter Name to Find Contact")

if st.button("Find Contact"):
    if find_name:
        response = requests.get(f"{api_url}/{find_name}")
        if response.status_code == 200:
            contact = response.json()
            st.write(f"Name: {contact['name']}, Number: {contact['number']}, City: {contact.get('city', 'N/A')}")
        else:
            st.error(f"Error: {response.json()['detail']}")
    else:
        st.error("Please enter a name")

# Display all contacts
st.header("All Contacts")
if st.button("Show All Contacts"):
    response = requests.get(api_url + "/")
    if response.status_code == 200:
        contacts = response.json()
        for contact in contacts:
            st.write(f"Name: {contact['name']}, Number: {contact['number']}, City: {contact.get('city', 'N/A')}")
    else:
        st.error("Failed to retrieve contacts")

# Update a contact
st.header("Update a Contact")
update_name = st.text_input("Name of Contact to Update")
new_number = st.text_input("New Number")
new_city = st.text_input("New City")

if st.button("Update Contact"):
    if update_name and new_number:
        updated_contact = {"name": update_name, "number": new_number, "city": new_city}
        response = requests.put(f"{api_url}/{update_name}", json=updated_contact)
        if response.status_code == 200:
            st.success("Contact updated successfully!")
        else:
            st.error(f"Error: {response.json()['detail']}")
    else:
        st.error("Name and New Number are required fields")

# Delete a contact
st.header("Delete a Contact")
delete_name = st.text_input("Name of Contact to Delete")

if st.button("Delete Contact"):
    if delete_name:
        response = requests.delete(f"{api_url}/{delete_name}")
        if response.status_code == 200:
            st.success("Contact deleted successfully!")
        else:
            st.error(f"Error: {response.json()['detail']}")
    else:
        st.error("Please enter a name")