
#Imports needed for the classification model
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from libsvm.svmutil import svm_train, svm_predict, svm_problem, svm_parameter

#Create the labels from the name audios stored in features_dict
def extract_labels_animals(features_extracted):
    labels_animals = []

    for file in features_extracted.keys():

        animal_name, _ = file.split('_', 1)

        dir_animal = "animals/segments/"

        print("ANIMAL: ",animal_name)

        if animal_name == f"{dir_animal}cat":
            labels_animals.append(0)
            print("LABEL 0")
        elif animal_name == f"{dir_animal}dog":
            labels_animals.append(1)
            print("LABEL 1")
        elif animal_name == f"{dir_animal}Kus":
            labels_animals.append(2)
            print("LABEL 2")
        elif animal_name == f"{dir_animal}inek":
            labels_animals.append(3)
            print("LABEL 3")
        elif animal_name == f"{dir_animal}maymun":
            labels_animals.append(4)
            print("LABEL 4")
        elif animal_name == f"{dir_animal}tavuk":
            labels_animals.append(5)
            print("LABEL 5")
        elif animal_name == f"{dir_animal}koyun":
            labels_animals.append(6)
            print("LABEL 6")

    print("TOTAL LABELS: ",labels_animals)
    return labels_animals
def prepare_features_animals(features_extracted):
    prepared_features = []
    for feature_dict in features_extracted.values():
        # Flatten the feature_dict into a single list
        flat_features = []
        for value in feature_dict.values():
            if isinstance(value, list) or isinstance(value, np.ndarray):
                flat_features.extend(value)
            else:
                flat_features.append(value)
        prepared_features.append(flat_features)
    return prepared_features
def split_train_test(features_animals, labels_animals):
    # Split data in train and test
    X_train, X_test, y_train, y_test = train_test_split(features_animals, labels_animals, test_size=0.2, random_state=42, stratify=labels_animals)
    return X_train, X_test, y_train, y_test

def classifier_SVM(X_train, X_test, y_train, y_test):
    # Create SVM classifier
    prob = svm_problem(y_train, X_train)
    param = svm_parameter('-t 0 -c 4 -b 1')  # -t 0 means linear kernel, -c 4 is the cost parameter, -b 1 enables probabilities

    print("training...")
    m = svm_train(prob, param)
    print("trained")

    # Predict labels for the test set
    p_label, p_acc, p_val = svm_predict(y_test, X_test, m)

    return p_label

def create_SVM2(features_extracted):
    print("Creating SVM model...")
    labels = extract_labels_animals(features_extracted)
    features_animals_prepared = prepare_features_animals(features_extracted)
    labels_animals_prepared = np.array(labels)
    X_train, X_test, y_train, y_test = split_train_test(features_animals_prepared, labels_animals_prepared)
    y_pred = classifier_SVM(X_train, X_test, y_train, y_test)

    # Print report classifier SVM
    print("SVM act Classifier Report")
    print(classification_report(y_test, y_pred))

    print("-"*200)
    # Print confusion matrix classifier SVM
    print("SVM Confusion Matrix")
    print(confusion_matrix(y_test, y_pred))

    return 0