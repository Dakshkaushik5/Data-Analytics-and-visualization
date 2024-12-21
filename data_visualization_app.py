import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("Interactive Data Visualization Tool")

# File uploader
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    # Load data
    data = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
    
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
    st.sidebar.warning("Please upload a CSV file to get started.")
    st.write("Upload a CSV file from the sidebar to start visualizing your data!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Python and Streamlit.")
