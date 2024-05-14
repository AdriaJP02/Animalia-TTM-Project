import subprocess
import streamlit
import os
from joblib import dump, load
from frontend.Main_Page import frontend_main_page
from dataset_creation.dataset_creation import create_dataset
from machinelearning_models.main_machinelearningmodels import run_machinelearningmodels
from feature_analysis.feature_analysis import feature_analysis
def main():

    # Dataset creation (Ubuntu)
    #create_dataset()

    # Feature analysis
    # Check if the features file already exists
    if os.path.exists('feature_analysis/features_dict.joblib'):
        # If the features file exists, load it
        features_extracted = load('feature_analysis/features_dict.joblib')
    else:
        # If the features file does not exist, extract the features and save them to a file
        features_extracted = feature_analysis()
        dump(features_extracted, 'feature_analysis/features_dict.joblib')

    # Run machine learning models
    run_machinelearningmodels(features_extracted)

    # Frontend
    #subprocess.run(["streamlit", "run","frontend/Main_Page.py"]) #In Windows
    #subprocess.run(["streamlit"srun", "./frontend/Main_Page.py"])  # In Ubuntu

if __name__ == "__main__":
    main()
