import streamlit as st
from PIL import Image
from streamlit_image_select import image_select

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
    #st.header("🔮️ Guessing Animal Sounds Game 🔮")
    st.image("frontend/GUI/TitolJoc2.png", use_column_width=True)

    st.write("En aquest joc hauràs d'endevinar quin animal està sonant.")
    st.image("frontend/GUI/AudioExemple.PNG", use_column_width=True)

    images = [
        "frontend/GUI/ImatgeMono.png",
        "frontend/GUI/ImatgeOvella.png",
        "frontend/GUI/ImatgeLleo.png",
        "frontend/GUI/ImatgePorc.png",
    ]
    captions = ["Mono", "Ovella", "Lleó", "Porc"]

    # Seleccionar animal
    img_index_aux = image_select(label="", images=images, captions=captions)


if __name__ == "__main__":
    main()
