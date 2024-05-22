import os

import numpy as np

import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from machinelearning_models.label_extraction import extract_labels_animals
import essentia.standard as es
from collections import Counter

import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split




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




def create_KNN2(extracted_features):
    # Assuming extract_labels_animals and prepare_features_animals functions are defined elsewhere

    labels, unique_labels = extract_labels_animals(extracted_features)
    features = prepare_features_animals(extracted_features)
    labels_encoded = np.array(labels)
    print(unique_labels)
    quit()
    exit()
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(np.array(features), labels_encoded, test_size=0.2, random_state=42)

    # Define and compile the neural network
    num_classes = len(unique_labels)


    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation=tf.keras.layers.LeakyReLU(alpha=0.2), input_shape=(X_train.shape[1],),
                              kernel_regularizer=regularizers.l1(0.001)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(32, activation=tf.keras.layers.LeakyReLU(alpha=0.2),
                              kernel_regularizer=regularizers.l1(0.001)),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])


    # Calculate class weights
    label_counts = Counter(y_train)
    total_samples = len(y_train)
    class_weights = {i: total_samples / (num_classes * count) for i, count in label_counts.items()}
    adam_optimizer = Adam(learning_rate=0.00005)  # Adjust the learning rate as needed

    model.compile(optimizer=adam_optimizer,
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=['accuracy'])


    # Train the model
    history = model.fit(X_train, y_train, epochs=5000, validation_data=(X_test, y_test), class_weight=class_weights)



    # Evaluate model on test data
    loss, accuracy = model.evaluate(X_test, y_test)

    # Print overall accuracy
    print("Overall Test Accuracy:", accuracy)
    # Calculate accuracy for each label
    label_accuracies = {}
    for label_idx in range(len(unique_labels)):
        label_test_indices = np.where(y_test == label_idx)[0]
        if len(label_test_indices) > 0:
            label_accuracy = model.evaluate(X_test[label_test_indices], y_test[label_test_indices], verbose=0)[1]
            label_accuracies[unique_labels[label_idx]] = label_accuracy

    # Print accuracy and number of samples for each label
    print("\nAccuracy and Number of Samples for Each Label:")
    for label_name, accuracy in label_accuracies.items():

        label_idx = unique_labels.index(label_name)
        label_test_indices = np.where(y_train == label_idx)[0]
        num_samples = len(label_test_indices)
        print(f"{label_name}: Accuracy - {accuracy}, Number of Samples - {num_samples}")


# Example call to function (ensure extracted_features is defined and properly formatted)
# create_KNN2(extracted_features)
