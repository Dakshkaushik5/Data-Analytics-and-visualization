import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc

# App title
st.title("Interactive Data Visualization Tool")

# Sidebar options
st.sidebar.header("Upload or Connect to Data")
data_source = st.sidebar.selectbox(
    "Choose Data Source",
    ["Upload CSV", "Upload Excel", "Connect to SQL Server"]
)

data = None  # Initialize the dataset

# If CSV file is selected
if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.sidebar.success("CSV file uploaded successfully!")

# If Excel file is selected
elif data_source == "Upload Excel":
    uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.sidebar.success("Excel file uploaded successfully!")

# If SQL Server is selected
elif data_source == "Connect to SQL Server":
    with st.sidebar.form("sql_connection_form"):
        server = st.text_input("Server Name")
        database = st.text_input("Database Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        table_name = st.text_input("Table Name")
        submit_button = st.form_submit_button("Connect")

    if submit_button:
        try:
            conn_str = (
                f"DRIVER={{SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
            conn = pyodbc.connect(conn_str)
            query = f"SELECT * FROM {table_name}"
            data = pd.read_sql(query, conn)
            conn.close()
            st.sidebar.success("Data fetched successfully from SQL Server!")
        except Exception as e:
            st.sidebar.error(f"Error connecting to SQL Server: {e}")

# If data is loaded successfully
if data is not None:
    # Display dataset preview
    st.header("Dataset Preview")
    st.dataframe(data.head())

    # Display dataset statistics
    st.header("Dataset Statistics")
    st.write(data.describe())

    # Visualization Options
    st.sidebar.header("Choose Visualization")
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"])

    # Select columns for visualizations
    st.sidebar.header("Choose Columns")
    x_col = st.sidebar.selectbox("Select X-Axis Column", data.columns)
    y_col = st.sidebar.selectbox("Select Y-Axis Column", data.columns)

    # Generate visualizations
    st.header("Visualization")
    if chart_type == "Line Chart":
        fig = px.line(data, x=x_col, y=y_col, title=f"{chart_type}: {y_col} vs {x_col}")
        st.plotly_chart(fig)
    elif chart_type == "Bar Chart":
        fig = px.bar(data, x=x_col, y=y_col, title=f"{chart_type}: {y_col} vs {x_col}")
        st.plotly_chart(fig)
    elif chart_type == "Scatter Plot":
        fig = px.scatter(data, x=x_col, y=y_col, title=f"{chart_type}: {y_col} vs {x_col}")
        st.plotly_chart(fig)
    elif chart_type == "Histogram":
        fig = px.histogram(data, x=x_col, title=f"{chart_type}: {x_col}")
        st.plotly_chart(fig)
else:
    st.write("No data loaded. Please select a data source and load your dataset.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Python and Streamlit.")
