#Imports needed for the classification model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle
from machinelearning_models.label_extraction import extract_labels_animals_new

#Create the labels from the name audios stored in features_dict
def extract_labels_animals(features_extracted):
    labels_animals = []
    dir_animal = "animals/segments/"

    for file in features_extracted.keys():
        animal_name, _ = file.split('_', 1)
        animal_name = animal_name.replace(dir_animal, "")
        print("ANIMAL: ", animal_name)

        if animal_name == "cat":
            labels_animals.append(0)
            print("LABEL 0")
        elif animal_name == "dog":
            labels_animals.append(1)
            print("LABEL 1")
        elif animal_name == "Kus":
            labels_animals.append(2)
            print("LABEL 2")
        elif animal_name == "inek":
            labels_animals.append(3)
            print("LABEL 3")
        elif animal_name == "maymun":
            labels_animals.append(4)
            print("LABEL 4")
        elif animal_name == "tavuk":
            labels_animals.append(5)
            print("LABEL 5")
        elif animal_name == "koyun":
            labels_animals.append(6)
            print("LABEL 6")
        elif animal_name == "aslan":
            labels_animals.append(7)
            print("LABEL 7")

    print("TOTAL LABELS: ", labels_animals)
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
    # Normalize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Apply PCA
    pca = PCA(n_components=0.95)  # Keep 95% of variance
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    # Create a SVM classifier with RBF kernel using the best parameters
    svm = SVC(C=100, coef0=0.0, degree=2, gamma=0.001,
    kernel='rbf', max_iter=5000, class_weight='balanced', verbose=1)

    # Train the classifier
    print("Training with PCA...")
    svm.fit(X_train, y_train)
    print("Training completed")

    # Save the model to disk
    filename = 'machinelearning_models/FinalSVM_model.sav'
    pickle.dump(svm, open(filename, 'wb'))

    print("SVM model saved.")

    # Predict the labels for the test set
    y_pred = svm.predict(X_test)

    return y_pred

def create_SVM(features_extracted):
    print("Creating SVM model...")
    labels, _  = extract_labels_animals_new(features_extracted)
    features_animals_prepared = prepare_features_animals(features_extracted)
    labels_animals_prepared = np.array(labels)
    X_train, X_test, y_train, y_test = split_train_test(features_animals_prepared, labels_animals_prepared)
    y_pred = classifier_SVM(X_train, X_test, y_train, y_test)

    # Print report for the classifier
    print("SVM Classifier Report")
    print(classification_report(y_test, y_pred))

    print("-" * 200)
    # Print confusion matrix for the classifier
    print("SVM Confusion Matrix")
    print(confusion_matrix(y_test, y_pred))

    return 0

# Example usage
# features_extracted = ... (load your feature extraction dictionary here)
# create_SVM(features_extracted)