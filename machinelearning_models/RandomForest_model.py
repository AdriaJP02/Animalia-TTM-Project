#Imports needed for the classification model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
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
    print("split1")
    # Split data in train and test
    X_train, X_test, y_train, y_test = train_test_split(features_animals, labels_animals, test_size=0.2, random_state=42)

    return  X_train, X_test, y_train, y_test


def classifier_RF(X_train, X_test, y_train, y_test):
    # Create a RandomForest classifier
    rf = RandomForestClassifier()

    # Create the parameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [300],
        'max_features': ['sqrt'],
        'max_depth': [50],
        'min_samples_split': [2],
        'min_samples_leaf': [1],
        'bootstrap': [False]
    }

    # Create the GridSearchCV object
    grid_search = GridSearchCV(rf, param_grid, cv=5, verbose=3, n_jobs=-1)

    # Train the classifier
    print("Training RandomForest...")
    grid_search.fit(X_train, y_train)
    print("Training completed")

    # Print the best parameters found by GridSearchCV
    print("Best parameters: ", grid_search.best_params_)

    # Print detailed results
    print("Grid search results:")
    means = grid_search.cv_results_['mean_test_score']
    stds = grid_search.cv_results_['std_test_score']
    params = grid_search.cv_results_['params']
    for mean, std, param in zip(means, stds, params):
        print(f"Mean: {mean:.3f}, Std: {std:.3f}, Params: {param}")
    print("Best parameters: ", grid_search.best_params_)
    # Save the model to disk
    filename = 'machinelearning_models/FinalRF_model.sav'
    pickle.dump(grid_search.best_estimator_, open(filename, 'wb'))
    print("Best parameters: ", grid_search.best_params_)
    print("RandomForest model saved.")

    # Predict the labels for the test set
    y_pred = grid_search.predict(X_test)

    return y_pred

def create_RF(features_extracted):
    print("Creating RF model...")
    labels, _ = extract_labels_animals_new(features_extracted)
    features_animals_prepared = prepare_features_animals(features_extracted)
    labels_animals_prepared = np.array(labels)
    X_train, X_test, y_train, y_test = split_train_test(features_animals_prepared, labels_animals_prepared)
    y_pred = classifier_RF(X_train, X_test, y_train, y_test)

    # Print report for the classifier
    print("RF Classifier Report")
    print(classification_report(y_test, y_pred))

    print("-" * 200)
    # Print confusion matrix for the classifier
    print("RF Confusion Matrix")
    print(confusion_matrix(y_test, y_pred))

    return 0
