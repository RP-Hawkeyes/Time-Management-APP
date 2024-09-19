import streamlit as st
import pandas as pd
import base64

# Dummy user data for login simulation
USER_DATA = {
    'production': {'password': 'prod123', 'role': 'Production'},
    'qa': {'password': 'qa123', 'role': 'QA'},
    'tl': {'password': 'tl123', 'role': 'TL'},
    'manager': {'password': 'mgr123', 'role': 'Manager'}
}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None

# Login function
def login(username, password):
    if username in USER_DATA and USER_DATA[username]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.role = USER_DATA[username]['role']
    else:
        st.error("Invalid username or password")

# Function to download CSV
def download_csv(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Encode as base64
    href = f'<a href="data:file/csv;base64,{b64}" download="time_management_data.csv">Download CSV</a>'
    return href

# Streamlit app
def main():
    st.title("Time Management Sheet")

    if not st.session_state.logged_in:
        # Login form
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            login(username, password)
    
    else:
        st.success(f"Logged in as {st.session_state.role}")
        
        # Display relevant data based on user role
        if st.session_state.role in ['Production', 'QA']:
            st.write("Welcome to the Time Management Sheet!")
            st.write("You have limited access.")
            # Example of limited functionality
            st.text_area("Log your hours worked:")
        elif st.session_state.role in ['TL', 'Manager']:
            st.write("Welcome to the Time Management Sheet!")
            st.write("You have full access.")
            # Example of full functionality
            data = pd.DataFrame({
                'Employee': ['Employee1', 'Employee2'],
                'Hours Worked': [8, 7]
            })
            st.dataframe(data)

            # Download CSV button
            st.markdown(download_csv(data), unsafe_allow_html=True)

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
