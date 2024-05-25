import streamlit as st
from PIL import Image
from st_audiorec import st_audiorec
#import tempfile
#import soundfile as sf
import os


st.set_page_config(
page_title="Imita animals",
page_icon="🎙",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
'Get Help': 'https://upf.edu/help',
'Report a bug': "https://upf.edu/bug",
'About': "# This is a header. This is *my first app*!"
}
)

# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode

def resize_image(image_input, custom_width, custom_height):
    # Read the image file
    image = Image.open(image_input)

    # Choose the resize option
    size = (custom_width, custom_height)

    resized_image = image.resize(size)

    # Display the resized image
    st.image(resized_image) #, caption="Resized Image")

def imitating_game():
    # Establecer el color de fondo
    page_bg_img = """
            <style>
            [data-testid="stAppViewContainer"]{
            background-color: #DFF4FE;
            opacity: 0.8;
            background-image: radial-gradient(#9ec2f4 0.5px, #DFF4FE 0.5px);
            background-size: 10px 10px;
            </style>
            """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    #resize_image(image_input="frontend/GUI/AnimaliaLogoMini.png", custom_width=120, custom_height=230)

    #st.header("🎙️ Imitating Animal Sounds Game 🎙️")
    st.image("frontend/GUI/TitolJoc3.png", use_column_width=True)

    st.write("En aquest joc hauràs d'imitar l'animal que vulguis.")

    #st.success('Data is loaded!')

    #st.success('Data/Models are loaded!')


    # Selectbox con nombres de animales y sus emojis
    animal_options = {
        "Gos 🐶": "🐶",
        "Gat 🐱": "🐱",
        "Ratolí 🐭": "🐭",
        "Conill 🐰": "🐰",
        "Vaca 🐮": "🐮",
        "Guineu 🦊": "🦊",
    }
    selected_animal = st.selectbox("Selecciona un animal:", list(animal_options.keys()))

    # Obtener el emoji del animal seleccionado
    selected_emoji = selected_animal #animal_options[selected_animal]
    st.write(f"Has seleccionat: {selected_emoji}")

    wav_audio_data = st_audiorec()

    # add some spacing and informative messages
    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer

    if wav_audio_data is not None:
        # output of percentages in animals
        st.image("frontend/GUI/PercentatgesAnimals.PNG", use_column_width=True)
        # Save the audio file
        save_path = 'frontend/temp_audios/TemporalAudio.wav'  # Change this to your desired path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(wav_audio_data)
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            st.audio(wav_audio_data, format='audio/wav')

if __name__ == "__main__":
    imitating_game()
