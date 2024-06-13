#https://essentia.upf.edu/essentia_python_examples.html
# I. Basic imports
import numbers
from joblib import dump, load
import os
import glob
import matplotlib.pyplot as plt
import essentia.standard as ess
import essentia.standard as es
import numpy as np

# II. Data Acquisition and Preprocessing
import urllib.request
import zipfile
import os, sys, shutil
from sklearn import preprocessing
import shutil

# III. Data Analysis
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif

# Import Warning
import warnings
warnings.filterwarnings('ignore')  # suppress warnings

# Global Variables for the Feature Analysis
main_data_dir = 'animals'

fs = 44100
windowSize = 2048 * 4
hopSize = 2048 * 2
NRG_threshold_ratio = 0.05

segments_dir = os.path.join(main_data_dir, 'segments')

# https://sites.google.com/site/gdocs2direct/

def load_data(main_data_dir, links, num_files=999):
    if not os.path.exists(main_data_dir):  # creating the directory if not exist
        os.mkdir(main_data_dir)
    for animal, url in links.items():
        #print('Downloading file for ', animal)
        targetDir = os.path.join(main_data_dir, animal)
        if not os.path.exists(targetDir):  # creating the director
            os.mkdir(targetDir)
        filename = url.split('/')[-1]
        urllib.request.urlretrieve(url, filename)
        # Unzipping to a specific folder
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(targetDir)
        zip_ref.close()
        os.remove(filename)  # Removing the zip file
        #print('Data downloaded and unzipped to: ', targetDir)

        # Keep only the first num_files files
        files = glob.glob(os.path.join(targetDir, '*'))
        for f in files[num_files:]:  # delete files from num_files onwards
            os.remove(f)

def create_file_lists(main_data_dir):
    """Collects file lists for each animal sound from the downloaded data.
    """
    animal_files = dict()
    for root, dirs, files in os.walk(main_data_dir):
        for file in files:
            # Only consider files ending with .wav or .aff in the filename
            if (file.endswith('.wav') or file.endswith('.aiff')):
                file_name = os.path.join(root, file)
                animal = file.split('.')[0]  # animal name is coded in the filename
                if len(animal) > 0:  # Avoid MACOS files starting with ._
                    files_animal = animal_files.get(animal)
                    if files_animal is None:
                        files_animal = [file_name]
                    else:
                        files_animal.append(file_name)
                    animal_files[animal] = files_animal
    return animal_files

def preprocess_data(animal_files, fs, windowSize, hopSize, NRG_threshold_ratio):
    fs = 44100

    if not os.path.exists('plot_animal_sounds'):
        os.makedirs('plot_animal_sounds')

    num_animals = len(animal_files.keys())

    file_ind_inlist = 0  # 0: let's take the first file in the list for sample plots
    for i, animal in enumerate(animal_files.keys()):
        sample_file = animal_files[animal][file_ind_inlist]
        #print("I: ", i),
        #print("ANIMAL: ", animal)
        x = ess.MonoLoader(filename=sample_file, sampleRate=fs)()

    params = {"fs": fs, "windowSize": windowSize, "hopSize": hopSize, "NRG_threshold_ratio": NRG_threshold_ratio}
    return params

def split_file(filename, params):
    '''Function to define split boundaries based on a fixed energy threshold
    '''
    x = ess.MonoLoader(filename=filename, sampleRate=fs)()
    NRG = []
    # Main windowing and feature extraction loop
    for frame in ess.FrameGenerator(x, frameSize=windowSize, hopSize=hopSize, startFromZero=True):
        NRG.append(ess.Energy()(frame))
    NRG = np.array(NRG)
    NRG = NRG / np.max(NRG)

    # Applying energy threshold to decide wave split boundaries
    split_decision_func = np.zeros_like(NRG)
    split_decision_func[NRG > NRG_threshold_ratio] = 1
    # Setting segment boundaries
    # Inserting a zero at the beginning since we will decide the transitions using a diff function
    split_decision_func = np.insert(split_decision_func, 0, 0)
    diff_split_decision = np.diff(split_decision_func)
    # Start indexes: transition from 0 to 1
    start_indexes = np.nonzero(diff_split_decision > 0)[0] * hopSize
    # Stop indexes: transition from 1 to 0
    stop_indexes = np.nonzero(diff_split_decision < 0)[0] * hopSize
    return (x, NRG, split_decision_func, start_indexes, stop_indexes)

def create_segments_dir(segments_dir, animal_files, params):
    if not os.path.exists(segments_dir):  # creating the directory
        os.mkdir(segments_dir)

    segment_files = []
    for animal, files in animal_files.items():
        file_count = 0
        for sample_file in files:
            x = ess.MonoLoader(filename=sample_file, sampleRate=fs)()
            (x, NRG, split_decision_func, start_indexes, stop_indexes) = split_file(sample_file, params)
            # Cropping segments
            for start, stop in zip(start_indexes, stop_indexes):
                if stop - start > fs/5:  # let's only keep segments larger than 1/5 second
                    x_seg = x[start: stop]
                    # Final check for amplitude (to avoid silent segments selection due to noise in split function)
                    if(np.max(np.abs(x_seg)) > 0.03):
                        # Amplitude normalization
                        x_seg = x_seg / np.max(np.abs(x_seg))
                        filename = os.path.join(segments_dir, animal + '_' + str(file_count) + '.wav')
                        ess.MonoWriter(filename=filename, format='wav', sampleRate=fs)(x_seg)
                        file_count += 1
                        segment_files.append(filename)
    return segment_files

def extract_features(segment_files):
    showPossibleFeatures = True
    features_dict = {}  # Create a dictionary to store the features

    for file in segment_files:
        # Use FreesoundExtractor
        extractor = es.FreesoundExtractor(lowlevelSilentFrames='drop',
                                          lowlevelFrameSize=2048,
                                          lowlevelHopSize=1024,
                                          lowlevelStats=['mean', 'stdev'])
        features, features_frames = extractor(file)

        # Store all lowlevel features in the dictionary
        features_dict[file] = {feature_name: features[feature_name]
                               for feature_name in features.descriptorNames()
                               if ('lowlevel' in feature_name or 'tonal' in feature_name)
                               and isinstance(features[feature_name], numbers.Number)}

    return features_dict  # Return the dictionary with the features

def get_label_from_filename(filename):
    # Suponiendo que el nombre del archivo está en el formato 'animal_<label>_<id>.wav'
    # Por ejemplo: 'animal_bird_01.wav'
    base_name = os.path.basename(filename).split('.')[0]  # Eliminar la extensión del archivo
    label = base_name.split('_')[0]  # Obtener la parte que contiene la etiqueta
    return label

def dict_to_numpy(features_dict):
    X = []
    y = []
    for file, features in features_dict.items():
        X.append(list(features.values()))
        y.append(get_label_from_filename(file))  # Función que obtiene la etiqueta desde el nombre del archivo
    return np.array(X), np.array(y)

def select_best_features(features_dict, k=10):
    X, y = dict_to_numpy(features_dict)
    selector = SelectKBest(score_func=f_classif, k=k)
    selector.fit(X, y)
    
    # Obtener los índices de las mejores características
    selected_indices = selector.get_support(indices=True)
    feature_names = list(next(iter(features_dict.values())).keys())
    selected_feature_names = [feature_names[i] for i in selected_indices]
    
    # Actualizar el diccionario con las mejores características
    for file in features_dict.keys():
        features_dict[file] = {name: features_dict[file][name] for name in selected_feature_names}
    
    return features_dict, selected_feature_names


def feature_analysis(links, k=10):
    main_data_dir = "tests" if "test" in links else "animals"

    if (not os.path.exists(main_data_dir)):
        for key, link in links.items():
            # Get the file extension
            _, file_extension = os.path.splitext(link)

            if file_extension in ['.wav', '.aiff']:  # if the links are wav or aiff extract the compressed audios
                main_data_dir = "tests"
                if not os.path.exists(main_data_dir):  # creating the directory if not exist
                    os.mkdir(main_data_dir)

                # Mover el archivo de audio a la nueva carpeta
                destination = os.path.join(main_data_dir, os.path.basename(link))
                shutil.move(link, destination)

            else:  # if the link is not an audio
                main_data_dir = "animals"
                load_data(main_data_dir, links)
                break

    segments_dir = os.path.join(main_data_dir, 'segments')

    animal_files = create_file_lists(main_data_dir)

    params = preprocess_data(animal_files, fs, windowSize, hopSize, NRG_threshold_ratio)

    segment_files = create_segments_dir(segments_dir, animal_files, params)

    features_dict = extract_features(segment_files)

    # Select the best features and update the features_dict
    features_dict, best_features = select_best_features(features_dict, k)

    return features_dict, best_features

