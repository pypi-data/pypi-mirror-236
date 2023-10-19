import streamlit as st
import requests
import openai
from unblockedGPT.rephrase import rephrase_2
from unblockedGPT.auth import Database
from unblockedGPT.detection import ai_detection, ai_detection_2
from unblockedGPT.typeresponse import Typeinator
from unblockedGPT.saveResponse import saveResponse
from unblockedGPT.projectDataTypes import Conversation, FullConversation, AIScore
from unblockedGPT.GPTHeroAuth import gptHeroAuthLogin, gptHeroSetTokes, gptHeroAuthSignUp
from streamlit_modal import Modal
import time
import sys


# Decrypted API keys
auth = Database.get_instance()
OPENAI_API_KEY_DEFAULT = auth.get_settings(0)
STEALTHGPT_API_KEY_DEFAULT = auth.get_settings(4)
GPTZERO_API_KEY_DEFAULT = auth.get_settings(5)

# Placeholder for special password
SPECIAL_PASSWORD = 'klfasdjf94305$'
DEFAULT_PW_KEY = "CC17F59E-1F6F-43EF-ACF4-A2B4B8E52401"

#get args from command line

savePath = sys.argv[1]

# Obtain API keys from the user (or use the defaults)
#openai_api_key = st.text_input("OpenAI Api Key", type="password")
#stealthgpt_api_key = st.text_input("Rephrasing Key", type="password")
#gptzero_api_key = st.text_input("Detection Key", type="password")
#orginality = st.text_input("Originality Key", type="password")
keys = [st.text_input(auth.key_lable(i), type="password") for i in auth.index if i != 2 and i != 3]
if st.button('Save Keys'):
    for i in range(len(keys)):
        if i != 2 and i != 3:
            if keys[i] != '' and keys[i] != None:
                auth.set_settings(i, keys[i])
                keys[i] = ''
    st.write("Keys Saved")
        

# Check if user entered the special password for any key
#if openai_api_key == SPECIAL_PASSWORD:
openai_api_key = OPENAI_API_KEY_DEFAULT
#if stealthgpt_api_key == SPECIAL_PASSWORD:
stealthgpt_api_key = STEALTHGPT_API_KEY_DEFAULT
#if gptzero_api_key == SPECIAL_PASSWORD:
gptzero_api_key = GPTZERO_API_KEY_DEFAULT

if 'modal' not in st.session_state:
    st.session_state.modal = 0
# Initialize session_state if not already initialized
if 'position' not in st.session_state:
    st.session_state.position = -1  # Position of the current display in history

if 'rephrase_list' not in st.session_state:
    st.session_state.rephrase_list = []
    st.session_state.submitFlag = True
# Title
st.title('Totally Not ChatGPT')
modal = Modal("", "testmodal")
open_modal = st.button("Sign-Up/Log-In to GPTHero")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        #write the is a modal in blue text
        st.write(f'<div style="color: blue;font-size: 30px;">Sign-Up for GPTHero</div>', unsafe_allow_html=True)
        if openai_api_key == False:
            st.write(f'<div style="color: blue;"><h2>OpenAI API Key</h2></div>', unsafe_allow_html=True)
            openai_api_key = st.text_input("OpenAI Api Key", type="password")
            submit = st.button("Submit")
            if submit:
                auth.set_settings(0, openai_api_key)
        else:
            col1, col2 = st.columns(2)
            with col1:
                loginButton = st.button("Login")
            with col2:
                signupButton = st.button("Sign-Up")
            if signupButton:
                st.session_state.modal = 2
            if loginButton:
                st.session_state.modal = 1
            if st.session_state.modal == 1:
                st.write(f'<div style="color: blue;font-size: 20px;">Login for GPTHero</div>', unsafe_allow_html=True)
                st.write("<div style='color: blue;'>Username</div>", unsafe_allow_html=True)
                username = st.text_input("", key="logusername")
                st.write("<div style='color: blue;'>Password</div>", unsafe_allow_html=True)
                password = st.text_input("", type="password", key= "logpassword")
                submitButton = st.button("Submit", key = "submitLogin")
                
                if submitButton:
                    login = gptHeroAuthLogin(username, password)
                    if login:
                        try:
                            auth.set_settings(2, username)
                            auth.set_settings(3, password)
                            #set the api keys
                            openai_api_key = auth.get_settings(0)
                            powerwritingaid_api_key = auth.get_settings(1)
                            if not powerwritingaid_api_key:
                                powerwritingaid_api_key = DEFAULT_PW_KEY
                            if gptHeroSetTokes(login, openai_api_key, powerwritingaid_api_key):
                                st.write("<div style='color: green;'>Logged in</div>", unsafe_allow_html=True)
                            else:
                                st.write("<div style='color: red;'>Error setting keys</div>", unsafe_allow_html=True)
                        except:
                            st.write("<div style='color: red;'>Error setting keys</div>", unsafe_allow_html=True)

                    else:
                        st.write("<div style='color: red;'>Invalid Username or Password</div>", unsafe_allow_html=True)

            
            if st.session_state.modal == 2:
                st.write(f'<div style="color: blue;font-size: 20px;">Sign-Up</div>', unsafe_allow_html=True)
                st.write("<div style='color: blue;'>Username</div>", unsafe_allow_html=True)
                username = st.text_input("", key = "username")
                st.write("<div style='color: blue;'>Password</div>", unsafe_allow_html=True)
                password = st.text_input("", type="password", key = "password")
                submitButton = st.button("Submit", key = "submitSignup")
                if submitButton:
                    if gptHeroAuthSignUp(username, password):
                        time.sleep(0.5)
                        login = gptHeroAuthLogin(username, password)
                        if login:
                            try:
                                auth.set_settings(2, username)
                                auth.set_settings(3, password)
                                openai_api_key = auth.get_settings(0)
                                powerwritingaid_api_key = auth.get_settings(1)
                                if not powerwritingaid_api_key:
                                    powerwritingaid_api_key = DEFAULT_PW_KEY
                                if gptHeroSetTokes(login, openai_api_key, powerwritingaid_api_key):
                                    st.write("<div style='color: green;'>Signed up and logged in</div>", unsafe_allow_html=True)
                                else:
                                    st.write("<div style='color: red;'>Error setting keys</div>", unsafe_allow_html=True)

                            except:
                                st.write("<div style='color: red;'>Error setting keys</div>", unsafe_allow_html=True)
                        else:
                            st.write("<div style='color: red;'>Error logging in</div>", unsafe_allow_html=True)
                    else:
                        st.write("<div style='color: red;'>Error signing up</div>", unsafe_allow_html=True)

                    

            
        close_modal = st.button("Close")
        if close_modal:
            st.session_state.modal = 0
            modal.close()
# Model selection
model_selection = st.selectbox('Select the model:', ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4'])

if st.button('Clear Conversation'):
    st.session_state.conversation = FullConversation()

# User input
user_input = st.text_area('You: ', height=200)
if 'conversation' not in st.session_state:
    st.session_state.conversation = FullConversation()

# Submit button
if st.button('Submit'):
    st.session_state.submitFlag = True

if user_input and st.session_state.submitFlag:
    st.session_state.submitFlag = False
    if openai_api_key != False:
        openai.api_key = openai_api_key
        try: 
            response = openai.ChatCompletion.create(
            model=model_selection,
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}]
        )
            chatbot_response = response['choices'][0]['message']['content'].strip()
            st.session_state.conversation.addResponse(user_input, chatbot_response, 1, AIScore(ai_detection( chatbot_response, auth), ai_detection_2( chatbot_response, auth)))
        except:
            st.write("Invalid API Key")
    else:
        st.write("Please enter an API Key")
        

        
# Rephrase button
if st.button('Rephrase Text'):
    if stealthgpt_api_key != False:
        headers = {'api-token': stealthgpt_api_key, 'Content-Type': 'application/json'}
        data = {'prompt': st.session_state.conversation.getConversation()[0].response, 'rephrase': True}
        response = requests.post('https://stealthgpt.ai/api/stealthify', headers=headers, json=data)
        if response.status_code == 200:
            rephrased_text = response.json()
            rephrased_text = rephrased_text['result']
            st.session_state.conversation.addResponse('Rephrase Text', rephrased_text, 0, AIScore(ai_detection( rephrased_text, auth), ai_detection_2( rephrased_text, auth)))
        elif response.status_code == 401:
            st.session_state.conversation.addResponse('Rephrase Text 1', 'Invalid API Key', 0, AIScore("N/A", "N/A"))
        else:
            st.session_state.conversation.addResponse('Rephrase Text 1', 'Could not rephrase', 0, AIScore("N/A", "N/A"))
    else:
        st.write("Please enter stealth API Key")

# Rephrase button 2
if st.button('Rephrase Text 2'):
    response =  rephrase_2(st.session_state.conversation.getConversation()[0].response)
    if response['status']:
        aiscore = AIScore(ai_detection( response['msg'], auth), ai_detection_2( response['msg'], auth))
    else:
        aiscore = AIScore("N/A", "N/A")
    st.session_state.conversation.addResponse('Rephrase Text 2', response['msg'], 0, aiscore)



# Type response
if st.button('Type Response'):
    #type the most recent, using keyboard inputs
    typeinator = Typeinator()
    time.sleep(5)
    typeinator.type(st.session_state.conversation.getConversation()[0].response)

st.write('Timed Typing')
minutes = st.number_input('Minutes to type response', min_value=0, max_value=1000, step=1)
if st.button('Timed Type Response') and minutes != 0:
    #type the most recent, using timed typing
    st.write('Typing in 5 seconds...')
    time.sleep(5)
    typeinator = Typeinator()
    typeinator.timeToType(st.session_state.conversation.getConversation()[0].response, minutes)
    minutes = 0


# Display conversation and rephrases
st.write(f'<div style="text-align: right; color: blue;">AI Detection Score: {st.session_state.conversation.getScore(1)}</div>', unsafe_allow_html=True )
st.write(f'<div style="text-align: right; color: blue;">AI Detection Score 2: {st.session_state.conversation.getScore(2)}</div>', unsafe_allow_html=True)
st.write("### Conversation:")
conversation = st.session_state.conversation.getConversation()
for turn in conversation:
    if turn.type == 1: 
        st.write(f'<div style="color: blue; background-color:{ "#E6EFFF" if turn.type == 1 else "#DFFFDF"}; padding: 10px; border-radius: 12px; margin: 5px;"><b>You:</b> {turn.prompt}</div>', unsafe_allow_html=True)
    st.write(f'<div style="color: black; background-color:{ "#DCDCDC " if turn.type == 1 else "#DFFFDF"}; padding: 10px; border-radius: 12px; margin: 5px;"><b>{"ChatGPT: " if turn.type == 1 else "Rephrase: "}</b> {turn.response} <br/> <div style="text-align: right; color: blue;">AI Detection Score: {turn.aiScore.score}<br>AI Detection Score 2:{turn.aiScore.score2}</div> </div>', unsafe_allow_html=True)
    if turn == conversation[0]:
        save = st.button('Save Response', key=turn.key)
        if save:
            if saveResponse(turn.response, savePath):
                st.write("Saved")
            else:
                st.write("Error saving")
    

