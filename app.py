
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
    

st.set_page_config(page_title="Staff Dashboard", layout="wide")

# Replace this with your actual file ID
# file_id = "1A2B3C4D5E6F7G8H9I0J"
# file_url = f"https://drive.google.com/uc?id={file_id}"
file_url = "https://docs.google.com/spreadsheets/d/1lWfTEhM4-aynLAlyQhkd0mO-KXD8cpZX/export?format=xlsx"


# Authentication (basic password)
# pwd = st.text_input("Enter password to access dashboard:", type="password")
# if pwd != "letmein123":
#     st.warning("🔒 Access Denied")
#     st.stop()

st.title("📋 CSA - HoR Regularization Exercise Summary")

# Load Excel file
#df = pd.read_excel(file_url, parse_dates=["DOB", "DOE"])
df = pd.read_excel(file_url, engine="openpyxl", parse_dates=["DOB", "DOE"])
#df.fillna("Not Provided", inplace=True)

# Sidebar filters
department = st.sidebar.selectbox("Choose Department", ["All"] + sorted(df["Department"].unique().tolist()))
sex = st.sidebar.radio("Sex", ["All", "M", "F"])
status = st.sidebar.radio("Pension Status", ["All", "Pension", "Active"])
sho_stat = st.sidebar.radio("Those who turned-up for the excercise", ["All", "Show", "No Show"])


filtered_df = df.copy()
if department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department]
if sex != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == sex]
if status != "All":
    filtered_df = filtered_df[filtered_df["Pension"] == status]
if sho_stat != "All":
    filtered_df = filtered_df[filtered_df["Availability"] == sho_stat]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Staff Reported to us", len(filtered_df[filtered_df["First_Name"].notna() & (filtered_df["First_Name"] != "")]))
col2.metric("💰 Avg. Salary", f"${filtered_df['Gross_Salary'].mean():,.2f}")
col3.metric("🧓 Avg. Age", round(filtered_df['Age'].mean(), 1))
col1.metric("🧓 Pension Status Count", filtered_df['Pension'].count())
col2.metric("🧓 Reported Positions", filtered_df['Availability'].count())

# Count Pension Status
pension_counts = filtered_df['Pension'].value_counts()
# Pie chart and bar chart side-by-side
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧓 Pension Status Breakdown")
    
    # Prepare data
    pension_counts = df['Pension'].value_counts().reset_index()
    pension_counts.columns = ['Pension Status', 'Count']
    pension_counts['Percentage'] = round(pension_counts['Count'] / pension_counts['Count'].sum() * 100, 1)
    pension_counts['Label'] = pension_counts.apply(lambda row: f"{row['Pension Status']}: {row['Count']} ({row['Percentage']}%)", axis=1)
    
    # Plot
    fig = px.pie(
        pension_counts,
        names="Label",
        values="Count",
        title="Pension vs Active Staff Breakdown",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='label+percent')
    
    st.plotly_chart(fig, use_container_width=True)



with col2:

    st.subheader("📊 Department-wise Headcount")
    
    dept_counts = filtered_df["Department"].value_counts().reset_index()
    dept_counts.columns = ['Department', 'Count']
    
    fig = px.bar(
        dept_counts,
        x="Department",
        y="Count",
        text="Count",
        color="Department",
        title="Headcount by Department",
        labels={"Count": "Number of Staff"}
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)





col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Highest Qualification Distribution")

    qual_counts = filtered_df["Qualification_Highest_Level"].value_counts().reset_index()
    qual_counts.columns = ['Qualification', 'Count']
    
    fig = px.bar(
        qual_counts,
        x="Qualification",
        y="Count",
        text="Count",
        color="Qualification",
        title="Highest Qualification Levels",
        labels={"Count": "Number of Staff"}
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)
    

with col2:
    #Data Table
    st.subheader("📑 Data Table")
    st.dataframe(filtered_df)

