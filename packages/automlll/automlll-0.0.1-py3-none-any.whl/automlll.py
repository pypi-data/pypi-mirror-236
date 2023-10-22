import streamlit as st
from streamlit_option_menu import option_menu

def main():
    st.title("🏠 Homebase")
    st.subheader("Welcome to the AutoML App")

    st.markdown("This app allows you to perform various tasks for automated machine learning and data analysis. "
                "Choose a task from the options below and follow the instructions to get started.")

    tasks = [
        "Upload_Data",
        "Feature_Engineering",
        "Regression",
        "Classification",
        "Clustering"
    ]

    selected_task = option_menu("Select a Task", 
                                tasks,orientation="horizontal",
                                icons=['cloud-upload-fill','clipboard-data-fill','bar-chart-line-fill','collection-fill','vr'],)

    if selected_task == "Upload_Data":
        st.subheader("Upload Your Dataset")
        st.markdown("Start by uploading your dataset. Supported file formats include CSV and Excel files. "
                    "Make sure your data is clean and well-structured for analysis.")
        st.image("images/upload_01.png", use_column_width=True)
        st.image("images/upload_02.png", use_column_width=True)
        st.image("images/upload_03.png", use_column_width=True)
        st.image("images/upload_04.png", use_column_width=True)
        st.info("You can find the 'Upload Data' page in the sidebar. Follow the steps to upload your dataset.")

    elif selected_task == "Feature_Engineering":
        st.subheader("Enhance Your Features")
        st.markdown("Feature engineering is essential for building accurate models. "
                    "Handle missing values, encode categorical variables, and create new features.")
        st.image("images/Feature_01.png", use_column_width=True)
        st.image("images/Feature_02.png", use_column_width=True)
        st.image("images/Feature_03.png", use_column_width=True)
        st.image("images/Feature_04.png", use_column_width=True)
        st.image("images/Feature_05.png", use_column_width=True)
        st.info("Visit the 'Feature Engineering' page to preprocess your data for modeling.")

    elif selected_task == "Regression":
        st.subheader("Build Regression Models")
        st.markdown("If you want to predict numeric values, use the Regression Model Maker. "
                    "Select your target variable and choose from various regression algorithms.")
        st.image("images/Regression_01.png", use_column_width=True)
        st.image("images/Regression_02.png", use_column_width=True)
        st.image("images/Regression_03.png", use_column_width=True)
        st.info("Go to the 'Regression Model Maker' page to train and evaluate regression models.")

    elif selected_task == "Classification":
        st.subheader("Create Classification Models")
        st.markdown("For classification tasks, the Classification Model Maker is your tool. "
                    "Select the target class and pick an algorithm to create predictive models.")
        st.image("images/Regression_04.png", use_column_width=True)
        st.info("Head to the 'Classification Model Maker' page to work with classification models.")

    elif selected_task == "Clustering":
        st.subheader("Explore Clustering Algorithms")
        st.markdown("Clustering helps discover patterns in your data. "
                    "Select a clustering algorithm and visualize your data clusters.")
        st.image("images/Clustering.png", use_column_width=True)
        st.image("images/Clustering_02.png", use_column_width=True)
        st.image("images/Clustering_03.png", use_column_width=True)
        st.info("Use the 'Clustering Model Maker' page to perform clustering analysis on your dataset.")

if __name__ == "__main__":
    main()

# pypi-AgENdGVzdC5weXBpLm9yZwIkNjI4YTFkMTAtYTg4Ni00ODdmLThiOWEtMzdjNGYyYmYzZmFhAAIqWzMsImU5ZjFiZGRiLTlhZGUtNDdhNy05YTE2LWNjMmFmOWIzOTk0MCJdAAAGIOsevceJarrhngveGCSH4VBMTX4DEIIIGfLE52ZOyjWb
