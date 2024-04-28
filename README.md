## Features & Specs
- Manage access to the user's microphone via the **browser's Media-API**
- Record, playback and revert audio-recordings in apps **deployed to the web**
- Download the final recording to your local system! - **WAV, 16 bit, 44.1 kHz**
- Directly return audio recording-data to Python backend! - **arrayBuffer format**<br>

## Setup & How to Execute
**1.** PIP Install the component
```
pip install streamlit
pip install streamlit-audiorec
```
If you have some problems installing them, then try to add " --user" at the end of the commands 

**2.** Execute the frontend part
```
# In Ubuntu
streamlit run ./Main_Page.py
# In Windows
streamlit run Main_Page.py
```
**3.** Modify the main.py
```
def main():
    # Execute the command "streamlit run frontend/Main_Page.py"
    subprocess.run(["streamlit", "run","frontend/Main_Page.py"]) #In Windows
    #subprocess.run(["streamlit", "run", "./frontend/Main_Page.py"])  # In Ubuntu
```
Comment and descomment this line depending on the operative system you are using