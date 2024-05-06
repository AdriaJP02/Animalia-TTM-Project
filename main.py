import subprocess
import streamlit
from frontend.Main_Page import frontend_main_page
from dataset_creation.dataset_creation import create_dataset
from machinelearning_models.main_machinelearningmodels import run_machinelearningmodels
from feature_analysis.feature_analysis import feature_analysis
def main():

    # Dataset creation (Ubuntu)
    create_dataset()

    # Feature analysis
    features_extracted = feature_analysis()

    # Run machine learning models
    #run_machinelearningmodels(features_extracted)
    run_machinelearningmodels(features_extracted)

    # Frontend
    #subprocess.run(["streamlit", "run","frontend/Main_Page.py"]) #In Windows
    #subprocess.run(["streamlit"srun", "./frontend/Main_Page.py"])  # In Ubuntu

if __name__ == "__main__":
    main()
