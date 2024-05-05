#https://essentia.upf.edu/essentia_python_examples.html
# I. Basic imports
import os
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

#Import Warning
import warnings
warnings.filterwarnings('ignore')  #suppress warnings


#Global Variables for the Feature Analysis
main_data_dir = 'animals'

fs = 44100
windowSize = 4096 * 4
hopSize = 4096 * 2
NRG_threshold_ratio = 0.01

segments_dir = os.path.join(main_data_dir,'segments')

def dataset_files():
    links = {'dog': 'https://drive.google.com/uc?export=download&id=1pNloKXlqHeu7SBNWTdQq3uNli4P8Io7q'}
    return links


def load_data(main_data_dir, links):

    if not os.path.exists(main_data_dir):  #creating the directory if not exist
        os.mkdir(main_data_dir)
    for animal, url in links.items():
        print('Downloading file for ', animal)
        targetDir = os.path.join(main_data_dir, animal)
        if not os.path.exists(targetDir):  #creating the director
            os.mkdir(targetDir)
        filename = url.split('/')[-1]
        urllib.request.urlretrieve(url, filename)
        #Unzipping to a specific folder
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(targetDir)
        zip_ref.close()
        os.remove(filename)  #Removing the zip file
        print('Data downloaded and unzipped to: ', targetDir)


def create_file_lists(main_data_dir):
    """Collects file lists for each animal sound from the downloaded data.
  """
    inst_files = dict()
    for root, dirs, files in os.walk(main_data_dir):
        for file in files:
            # Only consider files ending with .wav or .aff in the filename
            if (file.endswith('.wav') or file.endswith('.aiff')):
                file_name = os.path.join(root, file)
                instrument = file.split('.')[0]  # Instrument name is coded in the filename
                if len(instrument) > 0:  # Avoid MACOS files starting with ._
                    files_instrument = inst_files.get(instrument)
                    if files_instrument is None:
                        files_instrument = [file_name]
                    else:
                        files_instrument.append(file_name)
                    inst_files[instrument] = files_instrument
    return inst_files

def preprocess_data(inst_files,fs,windowSize,hopSize,NRG_threshold_ratio):
    fs = 44100

    num_animals = len(inst_files.keys())
    print("Sample waveform plots")
    plt.figure(1, figsize=(5 * num_animals, 3))
    file_ind_inlist = 0  # 0: let's take the first file in the list for sample plots
    for i, animal in enumerate(inst_files.keys()):
        sample_file = inst_files[animal][file_ind_inlist]
        x = ess.MonoLoader(filename=sample_file, sampleRate=fs)()

        plt.subplot(1, num_animals, (i + 1))
        plt.plot(x)
        plt.title(animal)


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

def create_segments_dir(segments_dir,inst_files,params):
    if not os.path.exists(segments_dir):#creating the directory
        os.mkdir(segments_dir)

    segment_files = []
    for instrument, files in inst_files.items():
        file_count = 0
        for sample_file in files:
            x = ess.MonoLoader(filename = sample_file, sampleRate = fs)()
            (x, NRG, split_decision_func, start_indexes, stop_indexes) = split_file(sample_file, params)
            #Croping segments
            for start, stop in zip(start_indexes, stop_indexes):
                if stop - start > fs/3:#let's only keep segments larger than 1/3 second
                    x_seg = x[start: stop]
                    #Final check for amplitude (to avoid silent segments selection due to noise in split function)
                    if(np.max(np.abs(x_seg)) > 0.05):
                        #Amplitude normalisation
                        x_seg = x_seg / np.max(np.abs(x_seg))
                        filename = os.path.join(segments_dir, instrument + '_' + str(file_count) + '.wav')
                        ess.MonoWriter(filename = filename, format = 'wav', sampleRate = fs)(x_seg)
                        file_count +=1
                        segment_files.append(filename)
    return segment_files

def extract_features(segment_files):
    showPossibleFeatures = True

    files = segment_files[:5]  # simply pick the first 5 files in the list
    for file in files:
        features, features_frames = es.MusicExtractor(lowlevelSilentFrames='drop',
                                                      lowlevelFrameSize=2048,
                                                      lowlevelHopSize=1024,
                                                      lowlevelStats=['mean', 'stdev'])(file)

        #scalar_lowlevel_descriptors = [descriptor for descriptor in features.descriptorNames() if
         #                              'lowlevel' in descriptor and isinstance(features[descriptor], float)]
        #return scalar_lowlevel_descriptors

        if(showPossibleFeatures):
            print("\nPossible features to analyze: ")
            print(sorted(features.descriptorNames()))
            print("-" * 200)

        print("File: ", file)
        print("Features extracted:\n")

        print("MFCC mean: ", features['lowlevel.mfcc.mean'])
        print("Spectral Centroid mean: ", features['lowlevel.spectral_centroid.mean'])
        print("Spectral Complexity mean: ", features['lowlevel.spectral_complexity.mean'])
        print("Dynamic Complexity: ", features['lowlevel.dynamic_complexity'])
        print("Loudness EBU128: ", features['lowlevel.loudness_ebu128.integrated'])
        print("Average Loudness: ", features['lowlevel.average_loudness'])
        print("Spectral Flux: ", features['lowlevel.spectral_flux.mean'])
        print("Spectral Centroid: ", features['lowlevel.spectral_centroid.mean'])
        print("Spectral Kurtosis: ", features['lowlevel.spectral_kurtosis.mean'])
        print("Spectral Spread: ", features['lowlevel.spectral_spread.mean'])
        print("Spectral Skewness: ", features['lowlevel.spectral_skewness.mean'])

        print("-"*200)
        showPossibleFeatures = False


def feature_analysis():
    print("Init Feature analysis...\n")

    links = dataset_files()
    print("Dataset Links Loaded.\n")

    load_data(main_data_dir,links)
    print("Data Loaded.")

    inst_files = create_file_lists(main_data_dir)
    print("List of files loaded: ", inst_files)
    print("\n")

    params = preprocess_data(inst_files, fs, windowSize, hopSize, NRG_threshold_ratio)
    print("Data preprocessed.\n")

    num_instruments = len(inst_files.keys())

    segment_files = create_segments_dir(segments_dir,inst_files, params)

    print(len(segment_files), 'Total animal segment files created.\n')

    extract_features(segment_files)
    print("Features Analysis finished.\n")

    return 0


