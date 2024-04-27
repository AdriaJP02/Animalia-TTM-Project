import streamlit as st

st.set_page_config(
page_title="Guessing Game",
page_icon="🔮️",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
'Get Help': 'https://upf.edu/help',
'Report a bug': "https://upf.edu/bug",
'About': "# This is a header. This is *my first app*!"
}
)

def main():

    st.title(':blue[ANIMAL]:violet[IA]')
    
    st.header("🔮️ Guessing Animal Sounds Game 🔮")

    st.write("In this game you are going to guess which animal sound is being played.")


if __name__ == "__main__":
    main()
