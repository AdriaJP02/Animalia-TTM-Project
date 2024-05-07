import streamlit as st
from PIL import Image
import io

st.set_page_config(
page_title="Animalia Main Page",
page_icon="🐮",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
'Get Help': 'https://upf.edu/help',
'Report a bug': "https://upf.edu/bug",
'About': "# This is a header. This is *my first app*!"
}
)

# Function to resize the image
def resize_image(image_input, custom_width, custom_height):
    # Read the image file
    image = Image.open(image_input)

    # Choose the resize option
    size = (custom_width, custom_height)

    resized_image = image.resize(size)

    # Display the resized image
    st.image(resized_image) #, caption="Resized Image")


def frontend_main_page():
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
    st.markdown( page_bg_img,unsafe_allow_html=True)

    #st.title(':blue[ANIMAL]:violet[IA]')
    #st.image("frontend/GUI/AnimaliaLogo.png", width=20, use_column_width=True)
    resize_image(image_input="frontend/GUI/AnimaliaLogo.png", custom_width=240, custom_height=460)
    st.write("**:blue[ANIMALIA]** és un **:blue[Joc de Sons d'Animals]** que té com a objectiu ser una eina útil per als **:blue[infants]** perquè aprenguin els sons d'animals.")
    st.write("És un projecte desenvolupat a l'assignatura de Taller de Tecnologia Musical a la UPF.")
    st.write("Conté 3 Fases de Jocs: \n")
    st.info("1) Escolta els animals 🔊️ \n")
    st.info("2) Endivina l'animal 🔮️ \n")
    st.info("3) Imita animals 🎙️")

    #Writing a sentence
    st.subheader("**Membres del Grup**")
    st.write("**Nom:** :blue[nom] **Correu:** :blue[mail]")
    
    st.header(" 🐶🐱🐮 ")

if __name__ == "__main__":
    frontend_main_page()
