import os
import subprocess
#from KNN_model import create_KNN
#from SVM_model import create_SVM
from machinelearning_models.SVM_model import create_SVM
from machinelearning_models.SVM_model2 import create_SVM2 # Importa la funció create_SVM del fitxer SVM_model
from machinelearning_models.KNN_model import create_KNN  # Importa la funció create_KNN del fitxer KNN_model
from machinelearning_models.KNN_model2 import create_KNN2 # Importa la funció create_KNN2 del fitxer KNN_model2
from machinelearning_models.RandomForest_model import create_RF  # Importa la funció create_RF del fitxer RandomForest_model
from machinelearning_models.NaiveBayes_model import create_NB
def run_machinelearningmodels(extracted_features):

    print("Running machine learning models")
    #print("Running KNN_1...\n")
    #create_KNN(extracted_features)
    #print("Running KNN_2...\n")
    #create_KNN2(extracted_features)
    #print("Running SVM...\n")
    #create_SVM(extracted_features)
    print("Running RF...\n")
    create_RF(extracted_features)
    print("Running NB...\n")
    create_NB(extracted_features)


    return 0
