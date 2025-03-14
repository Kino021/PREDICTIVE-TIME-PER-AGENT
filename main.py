import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(layout="wide", page_title="Daily Remark Summary", page_icon="📊", initial_sidebar_state="expanded")

# Apply dark mode
st.markdown(
    """
    <style>
    .reportview-container {
        background: #2E2E2E;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #2E2E2E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Daily Remark Summary')

@st.cache_data
def load_data(uploaded_file):
    # Load all the sheets into a dictionary of DataFrames
    xls = pd.ExcelFile(uploaded_file)
    call_history = pd.read_excel(xls, 'Call History')
    call_status_summary = pd.read_excel(xls, 'Call Status Summary')
    call_received_summary = pd.read_excel(xls, 'Call Received Summary')
    login_logout_activity = pd.read_excel(xls, 'Login Logout Activity')
    volare_status_summary = pd.read_excel(xls, 'Volare Status Summary')
    
    # Debugging step: Print out the columns in the "Login Logout Activity" sheet
    st.write("Columns in 'Login Logout Activity' sheet:", login_logout_activity.columns)

    return call_history, call_status_summary, call_received_summary, login_logout_activity, volare_status_summary

uploaded_file = st.sidebar.file_uploader("PREDICTIVE TIME PER AGENTS", type="xlsx")

if uploaded_file is not None:
    # Load the data from the uploaded file
    call_history, call_status_summary, call_received_summary, login_logout_activity, volare_status_summary = load_data(uploaded_file)

    # Check if 'Remark By' column exists in the 'call_history' DataFrame
    if 'Remark By' in call_history.columns:
        # Filter out unnecessary agents from 'Remark By' column
        call_history = call_history[~call_history['Remark By'].isin([ 
            'FGPANGANIBAN', 'KPILUSTRISIMO', 'BLRUIZ', 'MMMEJIA', 'SAHERNANDEZ', 'GPRAMOS',
            'JGCELIZ', 'JRELEMINO', 'HVDIGNOS', 'RALOPE', 'DRTORRALBA', 'RRCARLIT', 'MEBEJER',
            'DASANTOS', 'SEMIJARES', 'GMCARIAN', 'RRRECTO', 'JMBORROMEO', 'EUGALERA', 'JATERRADO'
        ])]
    else:
        st.warning("'Remark By' column not found in 'Call History' data.")

    # Function to calculate the total time spent per agent
    def calculate_total_time(df):
        # Convert the "Connect/Disconnect Date Time" to datetime format
        df['Connect/Disconnect Date Time'] = pd.to_datetime(df['Connect/Disconnect Date Time'], errors='coerce')
        
        # Make sure that the 'Collector' and 'Connect/Disconnect Date Time' columns exist
        if 'Collector' in df.columns and 'Connect/Disconnect Date Time' in df.columns:
            # Sort by Collector and Connect/Disconnect Date Time to correctly match Log In and Log Out events
            df = df.sort_values(by=['Collector', 'Connect/Disconnect Date Time'])
            
            # Calculate the time spent per row (difference between consecutive rows of Connect and Disconnect times)
            df['Time Spent'] = df.groupby('Collector')['Connect/Disconnect Date Time'].diff()

            # Remove any rows where time spent is NaN (first row for each Collector will be NaN)
            df = df.dropna(subset=['Time Spent'])

            # Sum the time spent per agent (sum times for the same 'Collector')
            total_time_per_agent = df.groupby('Collector')['Time Spent'].sum()

            # Convert the time spent to a more readable format (e.g., total hours and minutes)
            total_time_per_agent = total_time_per_agent.apply(lambda x: str(x))

            return total_time_per_agent
        else:
            st.error('Columns "Collector" or "Connect/Disconnect Date Time" not found in the data.')
            return None

    # Calculate total time for each agent in "Login Logout Activity"
    total_time_per_agent = calculate_total_time(login_logout_activity)

    # Display the total time per agent
    if total_time_per_agent is not None:
        st.write("Total Time Per Agent:", total_time_per_agent)
