import pickle
import numpy as np
import tempfile
import soundfile as sf
from feature_analysis.feature_analysis import feature_analysis
from machinelearning_models.RandomForest_model import prepare_features_animals
import librosa

# Load the model from disk: Random Forest
filenameRF = 'machinelearning_models/FinalRF_model.sav'
loaded_modelRF = pickle.load(open(filenameRF, 'rb'))

# Load the model from disk: SVM
filenameSVM = 'machinelearning_models/FinalSVM_model.sav'
loaded_modelSVM = pickle.load(open(filenameRF, 'rb'))

#Test1_Imitating: dog, sheep, cow
#link = {"test":"https://drive.google.com/uc?export=download&id=1iwh34dXFOm7m0hxFcA58TVxPAzt7cw7a"}

# Crear un archivo temporal
temp_file = tempfile.NamedTemporaryFile(delete=True)

# Guardar los datos de audio en el archivo temporal
wav_audio_data = 0
sf.write(temp_file.name, wav_audio_data, 44100)  # asumiendo una frecuencia de muestreo de 44100 Hz


# Define the path to the .wav file
#audio = "test/Voz-020.wav" #cow
#audio = "test/Voz-023.wav" #cat
audio = "test/Voz-024.wav"  #cat better
link = {"test": f"{audio}"}


# Load the .wav file
#test, sr = librosa.load(link, sr=None)
print("TEST: ", link)
new_audio_features = feature_analysis(link)
new_audio_features = prepare_features_animals(new_audio_features)

label_to_animal = {
    0: "cat",
    1: "dog",
    2: "bird",
    3: "cow",
    4: "monkey",
    5: "chicken",
    6: "sheep",
    7: "lion"
}

# Iterate over each feature vector in new_audio_features
print("RF model: \n")
for i, single_audio_features in enumerate(new_audio_features):
    # Convert the list of features to a numpy array
    single_audio_features_np = np.array(single_audio_features)
    # Reshape the numpy array as necessary
    single_audio_features_np = single_audio_features_np.reshape(1, -1)

    # Get the probabilities for each class
    probabilities = loaded_modelRF.predict_proba(single_audio_features_np)[0]

    # Get the indices of the top 3 classes with highest probability
    top3_indices = np.argsort(probabilities)[-3:][::-1]
    # Get the probabilities of the top 3 classes
    top3_probabilities = probabilities[top3_indices]

    # Print the top 3 classes with highest probability and their respective probabilities
    print(f"Top 3 predicted animals for audio {i + 1} using RF: ")
    for j in range(3):
        # Get the animal name corresponding to the class label
        predicted_animal = label_to_animal[top3_indices[j]]
        # Get the probability of the class
        probability = top3_probabilities[j]
        print(f"{j + 1}. {predicted_animal} (probability: {probability})")

print("\nSVM model: \n")
for i, single_audio_features in enumerate(new_audio_features):
    single_audio_features_np = np.array(single_audio_features)
    single_audio_features_np = single_audio_features_np.reshape(1, -1)  # reshape if necessary

    # Get the probabilities for each class
    probabilities = loaded_modelSVM.predict_proba(single_audio_features_np)[0]

    # Get the indices of the top 3 classes with highest probability
    top3_indices = np.argsort(probabilities)[-3:][::-1]
    # Get the probabilities of the top 3 classes
    top3_probabilities = probabilities[top3_indices]

    # Print the top 3 classes with highest probability and their respective probabilities
    print(f"Top 3 predicted animals for audio {i + 1} using SVM: ")
    for j in range(3):
        # Get the animal name corresponding to the class label
        predicted_animal = label_to_animal[top3_indices[j]]
        # Get the probability of the class
        probability = top3_probabilities[j]
        print(f"{j + 1}. {predicted_animal} (probability: {probability})")