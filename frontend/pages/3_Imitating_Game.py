import streamlit as st
from PIL import Image
from st_audiorec import st_audiorec
from main_imitating import imitating_animal
import os

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
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''', unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''', unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''', unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''', unsafe_allow_html=True)  # lightmode

def correspondingAnimals():
    # This is what will return the Test_model! (exact strings)
    # other strings: [cat, dog, bird, cow, monkey, chicken, sheep, lion]
    return ["cow", "dog", "bird"]

def resize_image(image_input, custom_width, custom_height):
    # Read the image file
    image = Image.open(image_input)

    # Choose the resize option
    size = (custom_width, custom_height)

    resized_image = image.resize(size)

    # Display the resized image
    st.image(resized_image) #, caption="Resized Image")
def translate_animal_name(animal):
    translations = {
        "cat": "Gat",
        "dog": "Gos",
        "bird": "Ocell",
        "cow": "Vaca",
        "monkey": "Mono",
        "chicken": "Gallina",
        "sheep": "Ovella",
        "lion": "Lleó"
    }
    return translations.get(animal, "Unknown")

def display_corresponding_images(predicted_animals):
    animals = predicted_animals
    image_paths = [f"frontend/GUI/Imatge{translate_animal_name(animal)}.png" for animal in animals]

    # Define sizes for the images
    sizes = [(400, 400), (170, 170), (100, 100)]

    # Display the images in a row
    col1, col2, col3 = st.columns(3)  # Create three columns

    # Display the images with different sizes in each column
    with col1:
        resize_image(image_paths[0], sizes[0][0], sizes[0][1])

    with col2:
        resize_image(image_paths[1], sizes[1][0], sizes[1][1])

    with col3:
        resize_image(image_paths[2], sizes[2][0], sizes[2][1])

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
        "Gallina 🐓": "🐓",
        "Lleó 🦁": "🦁",
        "Micu 🐒": "🐒",
        "Ocell 🐦": "🐦",
        "Ovella 🐑": "🐑",
        "Vaca 🐮": "🐮",
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
        # Save the audio file
        save_path = 'frontend/temp_audios/TemporalAudio.wav'  # Change this to your desired path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(wav_audio_data)
        predicted_animals = imitating_animal(save_path)

        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            st.audio(wav_audio_data, format='audio/wav')
        #st.image("frontend/GUI/PercentatgesAnimals.PNG", use_column_width=True)

        # Display the corresponding images
        display_corresponding_images(predicted_animals)

if __name__ == "__main__":
    imitating_game()
