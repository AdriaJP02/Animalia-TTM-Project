import pickle
import numpy as np
from feature_analysis.feature_analysis import feature_analysis
from machinelearning_models.RandomForest_model import prepare_features_animals
import shutil

# Initialize the variables to default values
top3_probabilities_rf = top3_probabilities_svm = None

# Initialize the result lists
results_rf = []
results_svm = []


#Transofrm the label number to animal
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

# Initialize dictionaries to store total probabilities and counts
total_probabilities_rf = {animal: 0 for animal in label_to_animal.values()}
total_counts_rf = {animal: 0 for animal in label_to_animal.values()}

total_probabilities_svm = {animal: 0 for animal in label_to_animal.values()}
total_counts_svm = {animal: 0 for animal in label_to_animal.values()}



def imitating_animal(save_path):

    # Load the model from disk: Random Forest
    filenameRF = 'machinelearning_models/FinalRF_model.sav'
    loaded_modelRF = pickle.load(open(filenameRF, 'rb'))

    # Load the model from disk: SVM
    filenameSVM = 'machinelearning_models/FinalSVM_model.sav'
    loaded_modelSVM = pickle.load(open(filenameRF, 'rb'))

    #Test1_Imitating: dog, sheep, cow
    #link = {"test":"https://drive.google.com/uc?export=download&id=1iwh34dXFOm7m0hxFcA58TVxPAzt7cw7a"}

    # Crear un archivo temporal
    temp_file_route = save_path  # Change this to your desired test path

    # Guardar los datos de audio en el archivo temporal
    #wav_audio_data = 0
    #sf.write(temp_file.name, wav_audio_data, 44100)  # asumiendo una frecuencia de muestreo de 44100 Hz


    # Define the path to the .wav file
    #audio = "test/Voz-020.wav" #cow
    #audio = "test/Voz-023.wav" #cat
    #audio = "test/Voz-024.wav"  #cat better
    link = {"test": f"{temp_file_route}"}


    # Load the .wav file
    #test, sr = librosa.load(link, sr=None)
    print("TEST: ", link)
    new_audio_features = feature_analysis(link)
    new_audio_features = prepare_features_animals(new_audio_features)



    # Iterate over each feature vector in new_audio_features
    #RF model
    for i, single_audio_features in enumerate(new_audio_features):
        # Convert the list of features to a numpy array
        single_audio_features_np = np.array(single_audio_features)
        # Reshape the numpy array as necessary
        single_audio_features_np = single_audio_features_np.reshape(1, -1)

        # Get the probabilities for each class
        probabilities = loaded_modelRF.predict_proba(single_audio_features_np)[0]

        # Get the indices of the top 3 classes with highest probability
        top3_indices_rf = np.argsort(probabilities)[-3:][::-1]
        # Get the probabilities of the top 3 classes
        top3_probabilities_rf = probabilities[top3_indices_rf]

        for j in range(3):
            # Get the animal name corresponding to the class label
            predicted_animal_rf = label_to_animal[top3_indices_rf[j]]
            # Get the probability of the class
            probability_rf = top3_probabilities_rf[j]

            # Add the probability to the total and increment the count
            total_probabilities_rf[predicted_animal_rf] += probability_rf
            total_counts_rf[predicted_animal_rf] += 1

    #SVM model
    for i, single_audio_features in enumerate(new_audio_features):
        single_audio_features_np = np.array(single_audio_features)
        single_audio_features_np = single_audio_features_np.reshape(1, -1)  # reshape if necessary

        # Get the probabilities for each class
        probabilities = loaded_modelSVM.predict_proba(single_audio_features_np)[0]

        # Get the indices of the top 3 classes with highest probability
        top3_indices_svm = np.argsort(probabilities)[-3:][::-1]
        # Get the probabilities of the top 3 classes
        top3_probabilities_svm = probabilities[top3_indices_svm]

        print(f"SVM probabilites Segmentations {i+1}:")
        for j in range(3):
            # Get the animal name corresponding to the class label
            predicted_animal_svm = label_to_animal[top3_indices_svm[j]]
            # Get the probability of the class
            probability_svm = top3_probabilities_svm[j]
            print(f"{j + 1}. {predicted_animal_svm} (probability: {probability_svm})")


            # Add the probability to the total and increment the count
            total_probabilities_svm[predicted_animal_svm] += probability_svm
            total_counts_svm[predicted_animal_svm] += 1

    average_probabilities_rf = {animal: total_probabilities_rf[animal] / total_counts_rf[animal]
                                for animal in total_probabilities_rf if total_counts_rf[animal] > 0}

    average_probabilities_svm = {animal: total_probabilities_svm[animal] / total_counts_svm[animal]
                                 for animal in total_probabilities_svm if total_counts_svm[animal] > 0}


    # Ordenar los resultados por probabilidad (de mayor a menor)
    sorted_results_rf = sorted(average_probabilities_rf.items(), key=lambda item: item[1], reverse=True)
    sorted_results_svm = sorted(average_probabilities_svm.items(), key=lambda item: item[1], reverse=True)

    print("\nRF results:", sorted_results_rf)
    print("SVM results:", sorted_results_svm)

    # Extraer solo las etiquetas de los animales TOP 3
    animal_labels_rf = [animal for animal, probability in sorted_results_rf[:3]]
    animal_labels_svm = [animal for animal, probability in sorted_results_svm[:3]]

    print("Final results RF TOP 3: ", animal_labels_rf)

    #Remove all stored files to keep privacy
    shutil.rmtree('tests')

    #return animal_labels_rf, animal_labels_svm
    return animal_labels_svm

test_path = 'frontend/temp_audios/TemporalAudio.wav'
results_svm = imitating_animal(test_path)

print("Final results SVM TOP 3 passed: ", results_svm)
