# Animal Sound Classification Project

## Overview
This project creates a machine learning model to classify animal sounds using a dataset from Freesound. The project includes dataset creation, audio processing, model development, and frontend development.

## Project Structure

### Dataset and Audio Processing
#### Dataset
- Download samples from the Google Drive folder

#### Audio Processing
- Slice audio samples.
- Extract features using Essentia.

#### Machine Learning Model
- Run extracted features through your choice of Machine Learning Model

### Frontend and Development Environment
#### Frontend
- Frontend UI developed with Streamlit.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AdriaJP02/Animalia-TTM-Project.git
    ```

2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script:
    ```bash
    python main.py
    ```

## Usage
- **Dataset Creation:** Initiate with `create_dataset`.
- **Feature Extraction:** Handle with `feature_analysis`. This also downloads the dataset if it is not available locally
- **Model Training:** Run and evaluate with `run_machinelearningmodels`.
- **Frontend:** Launch UI with Streamlit commands in the main script.

## Code Structure
- **dataset_creation:** Dataset creation scripts, creates JSON file for documentation.
- **feature_analysis:** Feature extraction scripts, and downloads sounds from google drive.
- **machinelearning_models:** Model development scripts, there are a variety of high-quality models in this folder.
- **frontend:** UI implementation scripts.
