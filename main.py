import subprocess
import streamlit
from frontend.Main_Page import frontend_main_page

def main():
    # Execute the command "streamlit run frontend/Main_Page.py"
    subprocess.run(["streamlit", "run","frontend/Main_Page.py"]) #In Windows
    #subprocess.run(["streamlit", "run", "./frontend/Main_Page.py"])  # In Ubuntu

if __name__ == "__main__":
    main()
