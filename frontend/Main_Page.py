import streamlit as st

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
def main():

    st.title(':blue[ANIMAL]:violet[IA]')
    st.header("**Main Page**")
    
    #The subheader
    st.subheader("**Description**")
    st.write("**:blue[ANIMAL]:violet[IA]** is an **:blue[Animal Sound Game]** that aims to be a useful tool for **:violet[children]** to learn animal sounds.")
    st.write("It is a project developed in the subject Music Technology Lab at UPF.")
    st.write("Consists in 3 Game Stages: \n")
    st.info("1) Reproducing Animal Sounds 🔊️ \n")
    st.info("2) Guessing Animal Sounds 🔮️ \n")    
    st.info("3) Imitating Animal Sounds 🎙️")

    #Writing a sentence
    st.subheader("**Team Members**")
    st.write("**Name:** :blue[name] **Mail:** :blue[mail]")
    
    st.header(" 🐶🐱🐮 ")

if __name__ == "__main__":
    main()
