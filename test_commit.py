import streamlit as st

# Task Class to hold task data
class Task:
    def __init__(self, name, description, frequency):
        self.name = name
        self.description = description
        self.frequency = frequency

# UserSettings Class to hold user data
class UserSettings:
    def __init__(self, first_name="", difficulty_level="Beginner"):
        self.first_name = first_name
        self.difficulty_level = difficulty_level

# Initialize session state variables if not already set
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "new_user" not in st.session_state:
    st.session_state["new_user"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "user_settings" not in st.session_state:
    st.session_state["user_settings"] = UserSettings()  # Default UserSettings object
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

# Welcome Page function
def welcome_page():
    st.title("PRACTONI")
    st.write("Returning User Login")
    st.text_input("Username: ", key="username")
    st.text_input("Password: ", type="password")
    
    if st.button("Login"):
        st.session_state["logged_in"] = True
        st.rerun()

    if st.button("New User? Create Account"):
        st.session_state["new_user"] = True
        st.rerun()
    
    st.write("Keep track of your practice!")
    st.write("Create tasks you hope to accomplish")

def new_user_welcome():
    st.title("Welcome, New User!")
    st.text_input("Enter your first name:", key="first_name")
    st.text_input("Enter a username: ", key="new_username")
    st.text_input("Enter a Password: ", type="password")

    user_settings = st.session_state["user_settings"]

    difficulty_level_input = st.selectbox(
    "Select Difficulty Level:", 
    ["Beginner", "Intermediate", "Advanced"], 
    index=["Beginner", "Intermediate", "Advanced"].index(user_settings.difficulty_level))
    user_settings.difficulty_level = difficulty_level_input

    if st.button("Create Account"):
        if st.session_state["first_name"] and st.session_state["new_username"]:
            # Create UserSettings object and save it in session state
            st.session_state["user_settings"] = UserSettings(
                first_name=st.session_state["first_name"], 
                difficulty_level= difficulty_level_input # Default difficulty level
            )
            st.session_state["username"] = st.session_state["new_username"]
            st.session_state["logged_in"] = True
            st.success("Account created!")
            st.rerun()
        else:
            st.error("Please fill in all fields.")
    
    

# User Settings Page
def user_settings_page():
    st.title("User Settings")
    
    # Access the UserSettings object
    user_settings = st.session_state["user_settings"]

    # Display and edit the user's first name and difficulty level
    first_name_input = st.text_input("Edit First Name:", value=user_settings.first_name)
    difficulty_level_input = st.selectbox(
        "Select Difficulty Level:", 
        ["Beginner", "Intermediate", "Advanced"], 
        index=["Beginner", "Intermediate", "Advanced"].index(user_settings.difficulty_level)
    )

    if st.button("Save Changes"):
        # Update UserSettings object in session state
        user_settings.first_name = first_name_input
        user_settings.difficulty_level = difficulty_level_input
        st.success("Settings updated successfully!")
        st.session_state["user_settings"] = user_settings  # Save updated settings back to session state
        st.session_state["user_settings_page"] = False  # Redirect back to tasks
        st.rerun()

    if st.button("Back to Tasks"):
        st.session_state["user_settings_page"] = False  # Redirect back to tasks
        st.rerun()

# Task Management (Add, Edit, Delete)
def tasks():
    st.title("Tasks:")

    if st.session_state["tasks"]:
        for task in st.session_state["tasks"]:
            st.write(f"**{task.name}**: {task.description} (Frequency: {task.frequency})")
    else:
        st.write("Welcome to the tasks page!")
        st.write("To add a task, click the 'Add a Task button!'")
        st.write("To edit a task, click the 'Edit a Task button!'")
        st.write("To change your preferred settings, click 'User Settings'")

    if st.button("Edit a Task"):
        st.session_state["edit_task"] = True
        st.rerun()

    if st.button("User Settings"):
        st.session_state["user_settings_page"] = True
        st.rerun()

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
            new_task = Task(task_name, task_description, frequency)
            st.session_state["tasks"].append(new_task)
            st.session_state["add_task"] = False
            st.success(f"Task '{task_name}' added successfully!")
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
            selected_task.name = task_name_input
            selected_task.description = task_description_input
            selected_task.frequency = frequency_input

            st.success(f"Task '{task_name_input}' updated successfully!")
            st.session_state["edit_task"] = False  # Reset edit task flag
            st.rerun()
        else:
            st.error("Please fill in both task name and description.")
    
    if st.button("Cancel"):
        st.session_state["edit_task"] = False
        st.rerun()

    # Delete task button
    if st.button("Delete Task"):
        st.session_state["delete_task"] = True
        st.session_state["task_to_delete"] = selected_task
        st.rerun()

def confirm_delete_task():
    st.warning(f"Are you sure you want to delete the task '{st.session_state['task_to_delete'].name}'? Removing this task cannot be undone and it will no longer appear in your 'Tasks' page.")

    if st.button("Delete"):
        # Delete the task from the session state
        task_to_delete = st.session_state["task_to_delete"]
        st.session_state["tasks"] = [task for task in st.session_state["tasks"] if task != task_to_delete]
        st.session_state["delete_task"] = False  # Exit delete confirmation
        st.success(f"Task '{task_to_delete.name}' deleted successfully!")
        st.session_state["edit_task"] = False
        st.rerun()  # Refresh the task list
    
    if st.button("Keep"):
        # If the user cancels, return to the edit task page
        st.session_state["delete_task"] = False
        st.rerun()  # Refresh the task list to go back to the edit page    

# Call the appropriate page based on user flow
if st.session_state.get("user_settings_page", False):
    user_settings_page()
elif st.session_state.get("delete_task", False):
    confirm_delete_task()
elif st.session_state.get("edit_task", False):
    edit_task_page()
elif st.session_state.get("add_task", False):
    add_task()
elif st.session_state["logged_in"]:
    tasks()
elif st.session_state["new_user"]:
    new_user_welcome()
else:
    welcome_page()
