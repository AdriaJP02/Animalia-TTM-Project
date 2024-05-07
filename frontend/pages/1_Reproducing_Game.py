import streamlit as st
from PIL import Image
#from Main_Page import resize_image
from streamlit_image_select import image_select
from pydub import AudioSegment
from io import BytesIO


st.set_page_config(
        page_title="Reproducing Game",
        page_icon="🔊️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def resize_image(image_input, custom_width, custom_height):
    # Read the image file
    image = Image.open(image_input)

    # Choose the resize option
    size = (custom_width, custom_height)

    resized_image = image.resize(size)

    # Display the resized image
    st.image(resized_image) #, caption="Resized Image")
def main():

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
    st.image("frontend/GUI/TitolJoc1.png", use_column_width=True)
    #st.header("🔊️ Escolta els animals 🔊️")

    st.write("En aquest joc reproduiràs els sons dels animals seleccionant l'animal que vulguis escoltar.")

    images = [
        "frontend/GUI/ImatgeMono.png",
        "frontend/GUI/ImatgeOvella.png",
        "frontend/GUI/ImatgeLleo.png",
        "frontend/GUI/ImatgePorc.png",
    ]
    captions = ["Mono", "Ovella", "Lleó", "Porc"]

    # Seleccionar animal
    img_index_aux = image_select(label="", images=images, captions=captions)
    img_dict = {
        "frontend/GUI/ImatgeMono.png": "Mono",
        "frontend/GUI/ImatgeOvella.png": "Ovella",
        "frontend/GUI/ImatgeLleo.png": "Lleó",
        "frontend/GUI/ImatgePorc.png": "Porc",
    }
    img_index = img_dict[img_index_aux]
    # Reproduir el so corresponent de l'animal seleccionat
    sound_links = {
        "Mono": "https://drive.google.com/file/d/1lXUOq98Pf1P2f--5_fsG_7aHlt2XZ6BO/view?usp=drive_link",
        "Ovella": "https://drive.google.com/file/d/1lXUOq98Pf1P2f--5_fsG_7aHlt2XZ6BO/view?usp=drive_link",
        "Lleó": "https://drive.google.com/file/d/1lXUOq98Pf1P2f--5_fsG_7aHlt2XZ6BO/view?usp=drive_link",
        "Porc": "https://drive.google.com/file/d/1lXUOq98Pf1P2f--5_fsG_7aHlt2XZ6BO/view?usp=drive_link",
    }
    #if img_index:
        #st.audio(sound_links[img_index], format='audio/wav')


if __name__ == "__main__":
    main()
