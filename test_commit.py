import streamlit as st

# User is not initially logged in
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# User is not initially a new user
if "new_user" not in st.session_state:
    st.session_state["new_user"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

if "edit_task" not in st.session_state:
    st.session_state["edit_task"] = False  # Initialize flag for editing a task


# Task Class to hold task data
class Task:
    def __init__(self, name, description, frequency):
        self.name = name
        self.description = description
        self.frequency = frequency

# Welcome Page function
def welcome_page():
    st.title("PRACTONI")
    st.write("Returning User Login")
    st.text_input("Username: ", key="username")
    st.text_input("Password: ", type="password")
    
    if st.button("Create Account"):
        st.session_state["new_user"] = True
        st.rerun()  # Forces the app to rerun and update the page
    
    st.write("Keep track of your practice!")
    st.write("Create tasks you hope to accomplish")

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
            st.rerun()  # Forces the app to rerun and update the page
        else:
            st.error("Please fill in all fields.")
    
def tasks():
    st.title("Tasks:")

    if st.session_state["tasks"]:
        for task in st.session_state["tasks"]:
            st.write(f"**{task.name}**: {task.description} (Frequency: {task.frequency})")
    else:
        st.write("Welcome to the tasks page!")
        st.write("To add a task, click the 'Add a Task' button!")
        st.write("To edit a task, click the 'Edit a Task' button!")
        st.write("To change your preferred settings, click 'User Settings'")
    
    if st.button("Edit a Task"):
        st.session_state["edit_task"] = True  # Set flag to true when editing task
        st.rerun()  # Rerun to show edit task form
    
    if st.button("Add a Task"):
        st.session_state["add_task"] = True
        st.rerun()

def add_task():
    st.title("Add a Task:")
    task_name = st.text_input("Task Name: ")
    task_description = st.text_area("Task Description: ")
    frequency = st.selectbox("Task Frequency", ["One-Time", "Daily", "Weekly"])

    if st.button("Confirm Changes"):
        if task_name and task_description:
            # Create task object and add it to the session state
            new_task = Task(task_name, task_description, frequency)
            st.session_state["tasks"].append(new_task)
            st.session_state["add_task"] = False
            st.success(f"Task '{task_name}' added successfully!")
            st.write(f"Description: {task_description}")
            st.write(f"Frequency: {frequency}")
            st.rerun()
        else:
            st.error("Please fill in both task name and description.")
    
    if st.button("Cancel"):
        st.session_state["add_task"] = False
        st.rerun()

def edit_task_page():
    st.title("Edit Task:")

    task_names = [task.name for task in st.session_state["tasks"]]
    task_name = st.selectbox("Select a task to edit", task_names)

    selected_task = next((task for task in st.session_state["tasks"] if task.name == task_name), None)

    if selected_task:
        task_name_input = st.text_input("Task Name:", selected_task.name)
        task_description_input = st.text_area("Task Description:", selected_task.description)
        frequency_input = st.selectbox("Task Frequency:", ["One-Time", "Daily", "Weekly"], index=["One-Time", "Daily", "Weekly"].index(selected_task.frequency))

        if st.button("Confirm Changes"):
            if task_name_input and task_description_input:
                # Update task object with new details
                selected_task.name = task_name_input
                selected_task.description = task_description_input
                selected_task.frequency = frequency_input

                st.success(f"Task '{task_name_input}' updated successfully!")
                st.session_state["edit_task"] = False  # Reset edit task flag
                st.rerun()  # Rerun to show tasks page again
            else:
                st.error("Please fill in both task name and description.")
        
        if st.button("Cancel"):
            st.session_state["edit_task"] = False
            st.rerun()  # Return to tasks page

# Call the function to display the page based on user flow
if st.session_state.get("edit_task", False):
    edit_task_page()  # Show the edit task page if user is editing
elif st.session_state.get("add_task", False):
    add_task()  # Show add task page
elif st.session_state["logged_in"]:
    tasks()  # Show tasks if logged in
elif st.session_state["new_user"]:
    new_user_welcome()  # Show new user page
else:
    welcome_page()  # Show welcome page
