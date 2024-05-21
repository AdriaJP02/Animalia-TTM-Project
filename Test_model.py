import pickle
import numpy as np
from feature_analysis.feature_analysis import feature_analysis
from machinelearning_models.RandomForest_model import prepare_features_animals

# Load the model from disk
filename = 'machinelearning_models/FinalRF_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

#Test1_Imitating: dog, sheep, cow
link = {"test":"https://drive.google.com/uc?export=download&id=1iwh34dXFOm7m0hxFcA58TVxPAzt7cw7a"}


new_audio_features = feature_analysis(link,True)
new_audio_features = prepare_features_animals(new_audio_features)

label_to_animal = {
    0: "cat",
    1: "dog",
    2: "bird",
    3: "cow",
    4: "monkey",
    5: "chicken",
    6: "sheep"
}

# Itera sobre cada vector de características en new_audio_features
for i, single_audio_features in enumerate(new_audio_features):
    single_audio_features_np = np.array(single_audio_features)
    single_audio_features_np = single_audio_features_np.reshape(1, -1)  # reshape if necessary
    result = loaded_model.predict(single_audio_features_np)
    predicted_animal = label_to_animal[result[0]]
    print(f"Prediction of the imitated animal for audio {i+1} using RF: ", predicted_animal)


