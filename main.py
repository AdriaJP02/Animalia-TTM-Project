import subprocess
import streamlit
import os
from joblib import dump, load
from frontend.Main_Page import frontend_main_page
from dataset_creation.dataset_creation import create_dataset
from machinelearning_models.main_machinelearningmodels import run_machinelearningmodels
from feature_analysis.feature_analysis import feature_analysis
from feature_analysis.feature_analysis_ori import feature_analysis_ori

def dataset_files():
    links = {'dog': 'https://drive.google.com/uc?export=download&id=1pNloKXlqHeu7SBNWTdQq3uNli4P8Io7q',
             'cat': 'https://drive.google.com/uc?export=download&id=1hlTTbC030SSFZ6Z3X38t43kjylAT5PFk',
             'Kus': 'https://drive.google.com/uc?export=download&id=1krCt4AnNB0lD9IyYU5oYX-4_jNEJsFa3',
             'inek': 'https://drive.google.com/uc?export=download&id=1Z0fK-A5X04VkkLxPh0nzrbOD-YlHljjW',
             'maymun':'https://drive.google.com/uc?export=download&id=1fGnxcfvtRYqJWo6bzgleFYRTON76JQ0y',
             'tavuk':'https://drive.google.com/uc?export=download&id=1Jjc-lR1__3jniHddsFMDOJjflmDK1R8c',
            'koyun':'https://drive.google.com/uc?export=download&id=17YjW-4twQt7QpENzbCDu8MUOTR6K_ra-'}
    return links

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
        links = dataset_files()
        features_extracted = feature_analysis(links)
        dump(features_extracted, 'feature_analysis/features_dict.joblib')

    # Run machine learning models
    run_machinelearningmodels(features_extracted)

    # Frontend
    #subprocess.run(["streamlit", "run","frontend/Main_Page.py"]) #In Windows
 	#subprocess.run(["streamlit", "run", "./frontend/Main_Page.py"])  # In Ubuntu

if __name__ == "__main__":
    main()
