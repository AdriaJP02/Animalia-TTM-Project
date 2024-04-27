import streamlit as st

st.set_page_config(
page_title="Reproducing Game",
page_icon="🔊️",
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
    
    st.header("🔊️ Reproducing Animal Sounds Game 🔊️")

    st.write("In this game you are going to reproduce animal sounds linked to their corresponding picture")


if __name__ == "__main__":
    main()
