import subprocess
import streamlit
import os
from joblib import dump, load
from frontend.Main_Page import frontend_main_page
from machinelearning_models.main_machinelearningmodels import run_machinelearningmodels
import platform

def dataset_files():
    links = {'dog': 'https://drive.google.com/uc?export=download&id=1pNloKXlqHeu7SBNWTdQq3uNli4P8Io7q',
             'cat': 'https://drive.google.com/uc?export=download&id=1hlTTbC030SSFZ6Z3X38t43kjylAT5PFk',
             'Kus': 'https://drive.google.com/uc?export=download&id=1krCt4AnNB0lD9IyYU5oYX-4_jNEJsFa3',
             'inek': 'https://drive.google.com/uc?export=download&id=1Z0fK-A5X04VkkLxPh0nzrbOD-YlHljjW',
             'maymun':'https://drive.google.com/uc?export=download&id=1fGnxcfvtRYqJWo6bzgleFYRTON76JQ0y',
             'tavuk':'https://drive.google.com/uc?export=download&id=1Jjc-lR1__3jniHddsFMDOJjflmDK1R8c',
             'koyun':'https://drive.google.com/uc?export=download&id=17YjW-4twQt7QpENzbCDu8MUOTR6K_ra-',
             'aslan':'https://drive.google.com/uc?export=download&id=1tVUoiRdhxyJ3KqlI1gcfcd2DCaxv7b4f'}
    return links

def main():

    # Dataset creation (Ubuntu)
    #create_dataset()

    # Feature analysis
    current_os = platform.system()
    print(current_os)



    frontend_on = False
    update = False



    # Run machine learning models

    #frontend
    ##doing it like this prevents windows users from accidently loading essentia

    if current_os == "Windows":
            features_extracted = load('feature_analysis/features_dict.joblib')
            run_machinelearningmodels(features_extracted)
            #subprocess.run(["streamlit", "run", "frontend/Main_Page.py"])
    elif current_os == "Linux" or current_os == "Darwin":
            from feature_analysis.feature_analysis import feature_analysis
            from feature_analysis.feature_analysis_ori import feature_analysis_ori
            if os.path.exists('feature_analysis/features_dict.joblib') and not update:
                    features_extracted = load('feature_analysis/features_dict.joblib')
            else:
                    # If the features file does not exist, extract the features and save them to a file
                    links = dataset_files()
                    features_extracted = feature_analysis(links)
                    dump(features_extracted, 'feature_analysis/features_dict.joblib')
            run_machinelearningmodels(features_extracted)
            #subprocess.run(["streamlit", "run", "./frontend/Main_Page.py"])
    else:
            raise OSError(f"Unsupported operating system: {current_os}")

if __name__ == "__main__":
    main()
