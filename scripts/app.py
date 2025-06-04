import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import os
from datetime import datetime

def save_uploaded_file(uploaded_file, save_path="data/uploads/"):
    """Save the uploaded file to disk"""
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def analyze_text_file(content):
    """Analyze text file content"""
    lines = content.split('\n')
    words = content.split()
    chars = len(content)
    
    return {
        'Total Lines': len(lines),
        'Total Words': len(words),
        'Total Characters': chars,
        'Average Words per Line': len(words) / len(lines) if lines else 0
    }

def analyze_csv_file(df):
    """Analyze CSV/Excel file content"""
    return {
        'Total Rows': len(df),
        'Total Columns': len(df.columns),
        'Column Names': df.columns.tolist(),
        'Missing Values': df.isnull().sum().to_dict(),
        'Data Types': df.dtypes.astype(str).to_dict()
    }

def main():
    st.set_page_config(page_title="Data Analysis Tool", page_icon="📊", layout="wide")
    
    st.title("📊 Interactive Data Analysis Tool")
    st.write("Upload your data files for instant analysis!")

    # File upload section
    uploaded_file = st.file_uploader(
        "Choose a file (TXT, CSV, XLSX, or other text-based files)",
        type=['txt', 'csv', 'xlsx', 'json', 'xml', 'log']
    )

    if uploaded_file is not None:
        # Save the file
        file_path = save_uploaded_file(uploaded_file)
        st.success(f"File uploaded successfully: {uploaded_file.name}")

        # File info
        st.subheader("📁 File Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**File Name:** {uploaded_file.name}")
        with col2:
            st.write(f"**File Type:** {uploaded_file.type}")
        with col3:
            st.write(f"**File Size:** {uploaded_file.size/1024:.2f} KB")

        # Process different file types
        if uploaded_file.type == "text/plain":
            # Text file analysis
            content = StringIO(uploaded_file.getvalue().decode()).read()
            analysis = analyze_text_file(content)
            
            st.subheader("📝 Text Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                for key, value in analysis.items():
                    st.write(f"**{key}:** {value}")
            
            with col2:
                # Word frequency visualization
                words = content.split()
                if words:
                    word_freq = pd.Series(words).value_counts().head(10)
                    fig, ax = plt.subplots()
                    word_freq.plot(kind='bar')
                    plt.title("Top 10 Most Common Words")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

        elif uploaded_file.type in ["application/vnd.ms-excel", 
                                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                  "text/csv"]:
            # CSV/Excel analysis
            try:
                if uploaded_file.type == "text/csv":
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.subheader("📊 Data Analysis")
                
                # Display basic information
                analysis = analyze_csv_file(df)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Basic Information:**")
                    for key, value in analysis.items():
                        if key not in ['Missing Values', 'Data Types']:
                            st.write(f"**{key}:** {value}")
                
                with col2:
                    st.write("**Data Types:**")
                    for col, dtype in analysis['Data Types'].items():
                        st.write(f"**{col}:** {dtype}")

                # Data Preview
                st.subheader("📋 Data Preview")
                st.dataframe(df.head())

                # Missing Values Visualization
                st.subheader("📉 Missing Values Analysis")
                missing_data = pd.DataFrame({
                    'Column': analysis['Missing Values'].keys(),
                    'Missing Values': analysis['Missing Values'].values()
                })
                
                if not missing_data.empty:
                    plt.clf()  # Clear any existing plots
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.set_style("whitegrid")  # Set style for better visibility
                    plot = sns.barplot(data=missing_data, x='Column', y='Missing Values', ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()  # Adjust layout to prevent label cutoff
                    
                    # Add value labels on top of each bar
                    for i, v in enumerate(missing_data['Missing Values']):
                        plot.text(i, v, str(v), ha='center', va='bottom')
                    
                    st.pyplot(fig)
                    
                    # Also display the missing values as a table for clarity
                    st.write("Missing Values Table:")
                    st.dataframe(missing_data)
                else:
                    st.info("No missing values found in the dataset! 🎉")

                # Numerical Columns Analysis
                numerical_cols = df.select_dtypes(include=[np.number]).columns
                if len(numerical_cols) > 0:
                    st.subheader("📈 Numerical Columns Analysis")
                    st.write(df[numerical_cols].describe())

                    # Correlation Matrix
                    if len(numerical_cols) > 1:
                        st.subheader("🔄 Correlation Matrix")
                        corr = df[numerical_cols].corr()
                        fig, ax = plt.subplots(figsize=(10, 8))
                        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
                        st.pyplot(fig)

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

        # Download processed data
        st.subheader("💾 Download Processed Data")
        if 'df' in locals():
            processed_csv = df.to_csv(index=False)
            st.download_button(
                label="Download processed data as CSV",
                data=processed_csv,
                file_name=f"processed_{uploaded_file.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main() 