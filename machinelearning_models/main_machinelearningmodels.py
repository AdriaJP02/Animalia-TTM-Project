import os
import subprocess
#from KNN_model import create_KNN
#from SVM_model import create_SVM
from machinelearning_models.SVM_model import create_SVM  # Importa la funció create_SVM del fitxer SVM_model
from machinelearning_models.KNN_model import create_KNN  # Importa la funció create_KNN del fitxer KNN_model

def run_machinelearningmodels(extracted_features):

    print("Running machine learning models")
    create_SVM(extracted_features)
    #create_KNN()

    return 0
