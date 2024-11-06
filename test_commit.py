import streamlit as st

# User is not initally logged in
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# User is not initally a new user
if "new_user" not in st.session_state:
    st.session_state["new_user"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# Welcome Page function
def welcome_page():
    # Display title and user inputs
    st.title("PRACTONI")
    st.write("Returning User Login")
    # Setting keys and types are crucial!!!
    st.text_input("Username: ", key="username")
    st.text_input("Password: ", type = "password")
    
    if st.button("Create Account"):
        st.session_state["new_user"] = True
        st.rerun()  # Forces the app to rerun and update the page

def new_user_welcome():
    st.title("Welcome, New User!")
    st.text_input("Enter your first name:", key="first_name")
    st.text_input("Enter a username: ", key="new_username")
    st.text_input("Enter a Password: ", type="password")

    if st.button("Create Account"):
        # Simulate account creation
        if st.session_state["first_name"] and st.session_state["new_username"]:
            st.session_state["logged_in"] = True
            st.success("Account created!")
        else:
            st.error("Please fill in all fields.")
    

# Call the function to display the new user registration page
if st.session_state["new_user"]:
    new_user_welcome()
else:
    welcome_page()