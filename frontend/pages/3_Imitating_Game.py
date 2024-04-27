import streamlit as st
from st_audiorec import st_audiorec

# DESIGN implement changes to the standard streamlit UI/UX
# --> optional, not relevant for the functionality of the component!

st.set_page_config(
page_title="Imitating Game",
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

def imitating_game():

    st.title(':blue[ANIMAL]:violet[IA]')
    
    st.header("🎙️ Imitating Animal Sounds Game 🎙️")

    st.write("In this game you are going to select an animal and then you will have to imitate its sound")

    #st.success('Data is loaded!')

    #st.success('Data/Models are loaded!')


    # Selectbox con nombres de animales y sus emojis
    animal_options = {
        "Dog 🐶": "🐶",
        "Cat 🐱": "🐱",
        "Mouse 🐭": "🐭",
        "Rabbit 🐰": "🐰",
        "Cow 🐮": "🐮",
        "Fox 🦊": "🦊",
    }
    selected_animal = st.selectbox("Select an animal:", list(animal_options.keys()))

    # Obtener el emoji del animal seleccionado
    selected_emoji = selected_animal #animal_options[selected_animal]
    st.write(f"You selected: {selected_emoji}")

    wav_audio_data = st_audiorec()

    # add some spacing and informative messages
    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer
        st.write('The .wav audio data, as received in the backend Python code,'
                 ' will be displayed below this message as soon as it has'
                 ' been processed. [This informative message is not part of'
                 ' the audio recorder and can be removed easily] 🎈')

    if wav_audio_data is not None:
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            st.audio(wav_audio_data, format='audio/wav')

if __name__ == "__main__":
    imitating_game()
