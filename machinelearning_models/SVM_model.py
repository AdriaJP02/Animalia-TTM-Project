#Imports needed for the classification model
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

#Create the labels from the name audios stored in features_dict
def extract_labels_animals(features_extracted):
    labels_animals = []

    for file in features_extracted.keys():
        animal_name, _ = file.split('_', 1)
        dir_animal = "animals/segments/"

        print("ANIMAL: ",animal_name)

        if animal_name == f"{dir_animal}dog":
            labels_animals.append(1)
            print("LABEL 1")
        elif animal_name == f"{dir_animal}cat":
            labels_animals.append(0)
            print("LABEL 0")
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
    svm = SVC(kernel='linear')

    # Train the classifier
    svm.fit(X_train, y_train)

    # Predict labels for the test set
    y_pred = svm.predict(X_test)

    return y_pred

def create_SVM(features_extracted):
    print("Creating SVM model...")

    labels = extract_labels_animals(features_extracted)

    features_animals_prepared = prepare_features_animals(features_extracted)
    labels_animals_prepared = np.array(labels)

    X_train, X_test, y_train, y_test = split_train_test(features_animals_prepared, labels_animals_prepared)

    y_pred = classifier_SVM(X_train, X_test, y_train, y_test)

    # Print report classifier SVM
    print(classification_report(y_test, y_pred))

    print("-"*200)
    # Print confusion matrix classifier SVM
    print(confusion_matrix(y_test, y_pred))

    return 0
