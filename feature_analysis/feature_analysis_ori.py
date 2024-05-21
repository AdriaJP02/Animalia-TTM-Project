# https://essentia.upf.edu/essentia_python_examples.html
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

# III. Data Analysis
import pandas as pd

# Import Warning
import warnings

warnings.filterwarnings('ignore')  # suppress warnings

# Global Variables for the Feature Analysis
main_data_dir = 'animals'

fs = 22050
windowSize = 2048 * 4
hopSize = 2048 * 2
NRG_threshold_ratio = 0.05

segments_dir = os.path.join(main_data_dir, 'segments')


# https://sites.google.com/site/gdocs2direct/
def dataset_files():
    links = {'dog': 'https://drive.google.com/uc?export=download&id=1pNloKXlqHeu7SBNWTdQq3uNli4P8Io7q',
             'cat': 'https://drive.google.com/uc?export=download&id=1hlTTbC030SSFZ6Z3X38t43kjylAT5PFk',
             'Kus': 'https://drive.google.com/uc?export=download&id=1krCt4AnNB0lD9IyYU5oYX-4_jNEJsFa3',
             'inek': 'https://drive.google.com/uc?export=download&id=1Z0fK-A5X04VkkLxPh0nzrbOD-YlHljjW',
             'maymun':'https://drive.google.com/uc?export=download&id=1fGnxcfvtRYqJWo6bzgleFYRTON76JQ0y',
             'tavuk':'https://drive.google.com/uc?export=download&id=1Jjc-lR1__3jniHddsFMDOJjflmDK1R8c',
             'koyun':'https://drive.google.com/uc?export=download&id=17YjW-4twQt7QpENzbCDu8MUOTR6K_ra-'}
    return links


def load_data(main_data_dir, links, num_files=999):
    if not os.path.exists(main_data_dir):  # creating the directory if not exist
        os.mkdir(main_data_dir)
    for animal, url in links.items():
        print('Downloading file for ', animal)
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
        print('Data downloaded and unzipped to: ', targetDir)

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

    # plt.figure(1, figsize=(5 * num_animals, 3))
    file_ind_inlist = 0  # 0: let's take the first file in the list for sample plots
    for i, animal in enumerate(animal_files.keys()):
        # plt.figure(i, figsize=(5, 3))
        sample_file = animal_files[animal][file_ind_inlist]
        print("I: ", i),
        print("ANIMAL: ", animal)
        x = ess.MonoLoader(filename=sample_file, sampleRate=fs)()

        # plt.plot(x)
        # plt.title(animal)
        # Save image of the plot in the plot_animal_sounds folder
        # plt.savefig(f'plot_animal_sounds/{animal}_output.png', dpi=100)
        # plt.close(i)

    # Let's put in a container to be able to use as a single argument in function calls
    params = {"fs": fs, "windowSize": windowSize, "hopSize": hopSize, "NRG_threshold_ratio": NRG_threshold_ratio}
    return params


def split_file(filename, params):
    '''Function to define split boundaries based on a fixed energy threshold
    '''
    x = ess.MonoLoader(filename=filename, sampleRate=fs)()
    NRG = [];
    #Main windowing and feature extraction loop
    for frame in ess.FrameGenerator(x, frameSize=windowSize, hopSize=hopSize, startFromZero=True):
        NRG.append(ess.Energy()(frame))
    NRG = np.array(NRG)
    NRG = NRG / np.max(NRG)

    #Applying energy threshold to decide wave split boundaries
    split_decision_func = np.zeros_like(NRG)
    split_decision_func[NRG > NRG_threshold_ratio] = 1
    #Setting segment boundaries
    #Inserting a zero at the beginning since we will decide the transitions using a diff function
    split_decision_func = np.insert(split_decision_func, 0, 0)
    diff_split_decision = np.diff(split_decision_func)
    #Start indexes: transition from 0 to 1
    start_indexes = np.nonzero(diff_split_decision > 0)[0] * hopSize
    #Stop indexes: transition from 1 to 0
    stop_indexes = np.nonzero(diff_split_decision < 0)[0] * hopSize
    return (x, NRG, split_decision_func, start_indexes, stop_indexes)

def create_segments_dir(segments_dir,animal_files,params):
    if not os.path.exists(segments_dir):#creating the directory
        os.mkdir(segments_dir)

    segment_files = []
    for animal, files in animal_files.items():
        file_count = 0
        for sample_file in files:
            x = ess.MonoLoader(filename = sample_file, sampleRate = fs)()
            (x, NRG, split_decision_func, start_indexes, stop_indexes) = split_file(sample_file, params)
            #Croping segments
            for start, stop in zip(start_indexes, stop_indexes):
                if stop - start > fs/5:#let's only keep segments larger than 1/5 second
                    x_seg = x[start: stop]
                    #Final check for amplitude (to avoid silent segments selection due to noise in split function)
                    if(np.max(np.abs(x_seg)) > 0.03):
                        #Amplitude normalisation
                        x_seg = x_seg / np.max(np.abs(x_seg))
                        filename = os.path.join(segments_dir, animal + '_' + str(file_count) + '.wav')
                        ess.MonoWriter(filename = filename, format = 'wav', sampleRate = fs)(x_seg)
                        file_count +=1
                        segment_files.append(filename)
    return segment_files

#SVM no funciona con FreesoundExtractor ni hardcoded ni filrando (queda en training)
#MusicExtractor con SVM y lowlevel y tonal error en inhomogeneous
#MusicExtractor hardcoded bien
#MusicExtractor con SVM y lowlevel solo se queda en training
#MusicExtractor hardcoded (7 clases, con 11 lowlevel features)

def extract_features(segment_files):
    showPossibleFeatures = True
    features_dict = {}  # Create a dictionary to store the features
    num_files_extracted = 5  # Number of files to extract features

    files = segment_files  # simply pick the first 5 files in the list
    for file in files:
        features, features_frames = es.MusicExtractor(lowlevelSilentFrames='drop',
                                                      lowlevelFrameSize=2048,
                                                      lowlevelHopSize=1024,
                                                      lowlevelStats=['mean', 'stdev'])(file)

        # Store the features in the dictionary
        features_dict[file] = {
            "MFCC mean": features['lowlevel.mfcc.mean'],
            "Spectral Centroid mean": features['lowlevel.spectral_centroid.mean'],
            "Spectral Complexity mean": features['lowlevel.spectral_complexity.mean'],
            "Dynamic Complexity": features['lowlevel.dynamic_complexity'],
            "Loudness EBU128": features['lowlevel.loudness_ebu128.integrated'],
            "Average Loudness": features['lowlevel.average_loudness'],
            "Spectral Flux": features['lowlevel.spectral_flux.mean'],
            "Spectral Centroid": features['lowlevel.spectral_centroid.mean'],
            "Spectral Kurtosis": features['lowlevel.spectral_kurtosis.mean'],
            "Spectral Spread": features['lowlevel.spectral_spread.mean'],
            "Spectral Skewness": features['lowlevel.spectral_skewness.mean']
        }

        showPossibleFeatures = False

    return features_dict  # Return the dictionary with the features

def feature_analysis_ori(update=False):
    print("Init Feature analysis...\n")

    if (not os.path.exists("animals")) or update:
        links = dataset_files()
        print("Dataset Links Loaded.\n")

        load_data(main_data_dir, links)
        print("Data Loaded.")

    animal_files = create_file_lists(main_data_dir)

    params = preprocess_data(animal_files, fs, windowSize, hopSize, NRG_threshold_ratio)
    print("Data preprocessed.\n")

    num_animals = len(animal_files.keys())
    segment_files = create_segments_dir(segments_dir, animal_files, params)
    print(len(segment_files), 'Total animal segment files created.\n')

    features_dict_ori = extract_features(segment_files)

    print("Features Analysis finished.\n")

    return features_dict_ori