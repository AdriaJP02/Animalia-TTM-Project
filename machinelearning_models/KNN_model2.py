import os

import numpy as np

import tensorflow as tf

import essentia.standard as es

import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split



# Define function to preprocess the audio files and extract features

def preprocess_data(data_dir, debug=False):

    features = []

    labels_encoded = []

    labels_names = []



    # Labels to be excluded
    excluded_labels = ['Chicken', 'Donkey', 'Frog', 'Monkey', 'Sheep','Cow']



    # Traverse through all subdirectories

    for root, dirs, files in os.walk(data_dir):

        for file in files:

            if file.lower().endswith('.wav'):

                audio_file = os.path.join(root, file)

                parent_folder = os.path.basename(os.path.dirname(audio_file))  # Get the immediate parent folder name

                grandparent_folder = os.path.basename(os.path.dirname(os.path.dirname(audio_file)))  # Get the grandparent folder name

                label = parent_folder if parent_folder != data_dir else grandparent_folder  # Use grandparent folder name if parent is the data_dir itself

                if label not in excluded_labels:

                    labels_names.append(label)

                    if debug:

                        print("Processing file:", audio_file, "Label:", label)  # Print filename and label

                    # Extract features from audio file

                    audio_features = extract_features(audio_file)



                    features.append(audio_features)



    # Encode labels to integers

    label_encoder = LabelEncoder()

    labels_encoded = label_encoder.fit_transform(labels_names)



    # Get unique labels and their counts

    unique_labels, counts = np.unique(labels_names, return_counts=True)



    return np.array(features), np.array(labels_encoded), unique_labels, counts



# Define the data directory

data_dir = "./"  # Update the data directory with the folder containing animal sounds



# Load and preprocess the data

features, labels_encoded, unique_labels, label_counts = preprocess_data(data_dir, debug=False)



# Split data into training and test sets

X_train, X_test, y_train, y_test = train_test_split(features, labels_encoded, test_size=0.2, random_state=42)



# Define and compile the neural network

num_classes = len(unique_labels)  # Calculate number of classes

model = tf.keras.Sequential([

    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),  # Input shape based on number of features

    tf.keras.layers.Dense(64, activation='relu'),

    tf.keras.layers.Dense(num_classes, activation='softmax')  # Softmax activation for multi-class classification

])



model.compile(optimizer='adam',

              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),  # Use from_logits=False when using softmax activation

              metrics=['accuracy'])



# Train the model

history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))



# Plot the loss for different labels

plt.figure(figsize=(10, 6))

for label_idx in range(len(unique_labels)):

    label = unique_labels[label_idx]

    label_indices = np.where(y_train == label_idx)[0]  # Get integer indices

    if len(label_indices) > 0:

        label_history = [history.history['loss'][idx] for idx in label_indices if idx < len(history.history['loss'])]

        plt.plot(label_history, label=f'Label {label}')

plt.title('Loss for Different Labels')

plt.xlabel('Epoch')

plt.ylabel('Loss')

plt.legend()

plt.show()



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

    label_index = np.where(unique_labels == label_name)[0][0]

    num_samples = label_counts[label_index]

    print(f"{label_name}: Accuracy - {accuracy}, Number of Samples - {num_samples}")



