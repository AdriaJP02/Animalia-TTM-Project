#Imports needed for the classification model
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from machinelearning_models.label_extraction import extract_labels_animals_new

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
    print("split1")
    # Split data in train and test
    X_train, X_test, y_train, y_test = train_test_split(features_animals, labels_animals, test_size=0.3, random_state=40)

    return  X_train, X_test, y_train, y_test


def classifier_NB(X_train, X_test, y_train, y_test):
    # Define priors
    priors = [0.1, 0.2, 0.3, 0.1, 0.1, 0.1, 0.1]  # these should add up to 1

    # Create classifier
    nb = GaussianNB()

    # Train the classifier
    nb.fit(X_train, y_train)

    # Predecir las etiquetas para el conjunto de prueba
    y_pred = nb.predict(X_test)

    return y_pred

def create_NB(features_extracted):
    print("Creating Naive Bayes model...")

    labels, _ = extract_labels_animals_new(features_extracted)

    features_animals_prepared = prepare_features_animals(features_extracted)
    #features_animals_prepared = features_extracted
    labels_animals_prepared = np.array(labels)

    X_train, X_test, y_train, y_test = split_train_test(features_animals_prepared, labels_animals_prepared)

    y_pred = classifier_NB(X_train, X_test, y_train, y_test)

    # Print report classifier NB
    print("Naive Bayes Classifier Report")
    print(classification_report(y_test, y_pred))

    print("-"*200)
    # Print confusion matrix classifier NB
    print("Naive Bayes Confusion Matrix")
    print(confusion_matrix(y_test, y_pred))

    print("-" * 200)

    return 0
