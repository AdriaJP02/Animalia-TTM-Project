import streamlit as st
from PIL import Image
from streamlit_image_select import image_select
import random
import time

st.set_page_config(
    page_title="Endevina l'animal",
    page_icon="🔮️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://upf.edu/help',
        'Report a bug': "https://upf.edu/bug",
        'About': "# This is a header. This is *my first app*!"
    }
)

# Map of image paths to audio paths
animal_sounds = {
    "frontend/GUI/ImatgeMono.png": "GameAudios/Micu.wav",
    "frontend/GUI/ImatgeOvella.png": "GameAudios/Ovella.wav",
    "frontend/GUI/ImatgeLleo.png": "GameAudios/Lleó.wav",
    "frontend/GUI/ImatgeVaca.png": "GameAudios/Vaca.wav",
    "frontend/GUI/ImatgeGat.png": "GameAudios/Gat.wav",
    "frontend/GUI/ImatgeGos.png": "GameAudios/Gos.wav",
    "frontend/GUI/ImatgeGallina.png": "GameAudios/Gallina.wav",
    "frontend/GUI/ImatgeOcell.png": "GameAudios/Ocell.wav"
}

animal_images = list(animal_sounds.keys())

# Function to play audio
def play_audio(audio_file):
    audio_bytes = open(audio_file, 'rb').read()
    st.audio(audio_bytes, format='audio/wav')

def main():


    st.image("frontend/GUI/TitolJoc2.png", use_column_width=True)
    st.write("En aquest joc hauràs d'endevinar quin animal està sonant.")
    st.image("frontend/GUI/AudioExemple.PNG", use_column_width=True)

    # Initialize session state for the game
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = random.choice(list(animal_sounds.values()))
        correct_image = list(animal_sounds.keys())[list(animal_sounds.values()).index(st.session_state.current_audio)]
        other_images = list(set(animal_images) - {correct_image})
        st.session_state.current_options = random.sample(other_images, 3) + [correct_image]
        random.shuffle(st.session_state.current_options)
        st.session_state.correct_image = correct_image
        st.session_state.image_selected = False  # Initialize control variable only if not initialized

    # Play current audio
    play_audio(st.session_state.current_audio)

    # Display animal image options
    selected_image = image_select(
        label="",
        images=st.session_state.current_options,
        captions=["Animal"] * 4
    )

    feedback_placeholder = st.empty()

    # Check if the selected image matches the current audio
    if selected_image:
        if animal_sounds[selected_image] == st.session_state.current_audio:

            feedback_placeholder.image("frontend/GUI/ImatgeCorrecte.png", use_column_width=True)
            time.sleep(1)
            feedback_placeholder.empty()
            st.success("Correcte! Has encertat l'animal.")
            #play_audio("frontend/ComplementaryAudios/CorrectAudio.wav")

            # Update to a new audio and options after correct selection
            remaining_images = list(set(animal_images) - {selected_image})
            st.session_state.current_audio = random.choice([animal_sounds[img] for img in remaining_images])
            correct_image = list(animal_sounds.keys())[
                list(animal_sounds.values()).index(st.session_state.current_audio)]
            other_images = list(set(animal_images) - {correct_image})
            st.session_state.current_options = random.sample(other_images, 3) + [correct_image]
            random.shuffle(st.session_state.current_options)
            st.session_state.correct_image = correct_image
        else:

            feedback_placeholder.image("frontend/GUI/ImatgeNoCorrecte.png", use_column_width=True)
            time.sleep(1)
            feedback_placeholder.empty()
            st.error("Incorrecte! Torna a provar.")
            #play_audio("frontend/ComplementaryAudios/NoCorrectAudio.wav")

if __name__ == "__main__":
    main()